import re
from typing import Optional
import json
from .config import _dict_update_deeply
from .config import load as load_config
from .logs import setup_log_config
import contextlib
import sys
import os
import traceback
import asyncio
from pathlib import Path
import inspect
import signal
import sys
from multiprocessing import Process
import aiohttp.web

# from aiohttp_devtools.runserver.watch import AppTask
from aiohttp.web_runner import AppRunner, TCPSite

from watchgod import awatch
from aiohttp import ClientSession
from importlib import import_module

import logging
main_logger = logging.getLogger('adev.main')
logger = logging.getLogger('adev.server.dft')
aux_logger = logging.getLogger('adev.server.aux')


def run_app(app_factory, working_directory, host=None, port=8000, verbose=False):

    # force a full reload in sub processes so they load an updated version of code,
    # this must be called only once
    from multiprocessing import set_start_method
    set_start_method('spawn')

    app_factory_module = inspect.getmodule(app_factory)
    app_factory_pyfile = Path(app_factory_module.__file__).resolve()
    app_factory_name = app_factory.__name__

    config = Config(
        python_path=working_directory,
        watch_path=working_directory,
        py_file=Path(app_factory_pyfile).resolve(),
        app_factory_name=app_factory_name,
        port=port,
        host=host,
        verbose=verbose
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_port_open(host, config.port, loop))

    main_manager = WatchedAppTask(config, loop)
    loop.run_until_complete(main_manager.start())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    except RunnerException as e:
        main_logger.error('Error: %s', e)
        sys.exit(2)
    finally:
        main_logger.info('shutting down server...')
        start = loop.time()
        with contextlib.suppress(asyncio.TimeoutError, KeyboardInterrupt):
            loop.run_until_complete(main_manager.close())
        main_logger.info('shutdown took %0.2fs', loop.time() - start)


class RunnerException(Exception):
    pass


class Config:
    def __init__(self, *,
                 python_path: str = None,
                 watch_path: str = None,
                 app_factory_name: str = None,
                 py_file: str = None,
                 host: str = "localhost",
                 port: int = 8000,
                 verbose: bool = False):

        self.python_path = python_path
        self.watch_path = watch_path
        self.py_file = py_file
        self.app_factory_name = app_factory_name
        self.host = host
        self.port = port
        self.verbose = verbose

        logger.debug(f"config loaded: {self}")

    def import_app_factory(self):

        # 每次进程启动，需要覆盖logging的配置
        setup_log_config(
            verbose=self.verbose,
            is_production_mode=False
        )

        rel_py_file = self.py_file.relative_to(self.python_path)
        module_path = '.'.join(rel_py_file.with_suffix('').parts)

        sys.path.append(str(self.python_path))

        try:
            module = import_module(module_path)
        except ImportError as exc:
            msg = (
                f"error importing '{module_path}' from '{self.python_path}': {exc}")
            raise RunnerException(msg) from exc

        try:
            attr = getattr(module, self.app_factory_name)
        except AttributeError as exc:
            msg = (f"Module '{module.__name__}' does not define a "
                   f"'{self.app_factory_name}' attribute/class")
            raise RunnerException(msg) from exc

        return attr

    async def load_app(self):
        app_factory = self.import_app_factory()

        if isinstance(app_factory, aiohttp.web.Application):
            app = app_factory
        else:
            # app_factory should be a proper factory with signature (loop): -> Application
            signature = inspect.signature(app_factory)
            if 'loop' in signature.parameters:
                loop = asyncio.get_event_loop()
                app = app_factory(loop=loop)
            else:
                # loop argument missing, assume no arguments
                app = app_factory()

            if asyncio.iscoroutine(app):
                app = await app

            if not isinstance(app, aiohttp.web.Application):
                errmsg = (f"app factory '{self.app_factory_name}' returned "
                          f"'{app.__class__.__name__}' not an aiohttp.web.Application")
                raise RunnerException(errmsg)

        return app


class WatchedAppTask:
    def __init__(self, config: Config, loop: asyncio.AbstractEventLoop):
        self._config = config
        self._loop = loop

        self._reloads = 0
        self._runner = None
        self._task = None

        assert self._config.watch_path
        self.stopper = asyncio.Event(loop=self._loop)
        self._awatch = awatch(self._config.watch_path, stop_event=self.stopper)


    async def start(self):
        self._task = self._loop.create_task(self._run())

    async def close(self, *args):
        self.stopper.set()
        self._stop_dev_server()

        if self._task:
            self.stopper.set()
            async with self._awatch.lock:
                if self._task.done():
                    self._task.result()
                self._task.cancel()

    async def _run(self, live_checks=20):
        try:
            self._start_dev_server()

            async for changes in self._awatch:
                self._reloads += 1
                if any(f.endswith('.py') for _, f in changes):
                    logger.debug('%d changes, restarting server', len(changes))
                    self._stop_dev_server()
                    self._start_dev_server()

        except Exception as exc:
            logger.exception(exc)
            raise RunnerException('error running dev server')

    def _start_dev_server(self):
        act = 'Start' if self._reloads == 0 else 'Restart'
        logger.info(
            f"{act}ing dev server at http://{self._config.host}:{self._config.port} ●")

        self._process = Process(target=serve_main_app, args=(self._config,))
        self._process.start()

    def _stop_dev_server(self):
        if self._process.is_alive():
            logger.debug('stopping server process...')
            os.kill(self._process.pid, signal.SIGINT)
            self._process.join(5)
            if self._process.exitcode is None:
                logger.warning('process has not terminated, sending SIGKILL')
                os.kill(self._process.pid, signal.SIGKILL)
                self._process.join(1)
            else:
                logger.debug('process stopped')
        else:
            logger.warning(
                'server process already dead, exit code: %s', self._process.exitcode)


async def check_port_open(host, port, loop, delay=1):
    # the "s = socket.socket; s.bind" approach sometimes says a port is in use when it's not
    # this approach replicates aiohttp so should always give the same answer
    for i in range(5, 0, -1):
        try:
            server = await loop.create_server(asyncio.Protocol(), host=host, port=port)
        except OSError as e:
            if e.errno != 98:  # pragma: no cover
                raise
            main_logger.warning(
                f"port {port} is already in use, waiting {i}...")
            await asyncio.sleep(delay, loop=loop)
        else:
            server.close()
            await server.wait_closed()
            return
    raise RunnerException(f"The port {port} at {host} has already be used")


def serve_main_app(config: Config):

    loop = asyncio.get_event_loop()
    runner = loop.run_until_complete(start_main_app(config, loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:  # pragma: no cover
        pass
    finally:
        with contextlib.suppress(asyncio.TimeoutError, KeyboardInterrupt):
            loop.run_until_complete(runner.cleanup())


async def start_main_app(config: Config, loop):

    app = await config.load_app()

    host = "localhost"
    log_format = '%a (%{X-Real-IP}i) %t "%r" %s %b "%{Referer}i" "%{User-Agent}i"'

    await check_port_open(host, config.port, loop)
    runner = aiohttp.web.AppRunner(app, access_log_format=log_format)
    await runner.setup()
    site = aiohttp.web.TCPSite(
        runner, host=host, port=config.port, shutdown_timeout=0.1)
    await site.start()
    return runner
