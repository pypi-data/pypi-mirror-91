import os
import argparse
import aiohttp.web
import inspect
from pathlib import Path

from .config import setup as setup_config
from .config import setup_logging
from .dev_tools import run_app as dev_run_app
from .logs import setup_log_config


def cli(app_factory):

    app_factory_module = inspect.getmodule(app_factory)
    app_factory_pyfile = Path(app_factory_module.__file__).resolve()
    working_directory = app_factory_pyfile.parent.resolve()

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-H", "--host",
        help="TCP/IP host to serve on (default: %(default)r)",
        default="localhost"
    )
    arg_parser.add_argument(
        "-p", "--port",
        help="TCP/IP port to serve on (default: %(default)r)",
        type=int,
        default="8000"
    )
    arg_parser.add_argument('--production', action='store_true',
                            help='to enable production environment')

    arg_parser.add_argument(
        "--working-directory",
        help=f"Working directory(default: '{working_directory}')",
        type=str,
        default=working_directory
    )

    arg_parser.add_argument('--verbose', action='store_true',
                            help='to show logging configuration')

    args = arg_parser.parse_args()

    if args.production:
        os.environ['PYTHON_ENV'] = 'production'

    if args.port:
        os.environ['PORT'] = str(args.port)

    os.chdir(args.working_directory)

    setup_config(directory='conf')

    if args.production:
        setup_log_config(verbose=args.verbose, is_production_mode=True)

        log_format = '%a (%{X-Real-IP}i) %t "%r" %s %b "%{Referer}i" "%{User-Agent}i"'
        aiohttp.web.run_app(app_factory(),
                            host=args.host,
                            port=args.port,
                            access_log_format=log_format)
    else:
        setup_log_config(verbose=args.verbose, is_production_mode=False)

        dev_run_app(app_factory, working_directory=working_directory,
                    host=args.host, port=args.port)
