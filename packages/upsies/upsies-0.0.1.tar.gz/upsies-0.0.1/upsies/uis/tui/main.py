"""
Entry point
"""

import sys

from ... import __homepage__, __project_name__, defaults, errors
from ...utils import configfiles
from .args import parse as parse_args
from .commands import CommandBase
from .ui import UI

import logging  # isort:skip
_log = logging.getLogger(__name__)


def main(args=None):
    sys.exit(_main(args))


def _main(args=None):
    # Read CLI arguments
    # argparse has sys.exit(2) hardcoded for CLI errors.
    try:
        args = parse_args(args)
    except SystemExit:
        return 1

    if args.debug:
        logging.basicConfig(
            format='%(asctime)s: %(name)s: %(message)s',
            filename=args.debug,
        )
        logging.getLogger(__project_name__).setLevel(level=logging.DEBUG)

    # Read config files
    try:
        cfg = configfiles.ConfigFiles(defaults=defaults.defaults)
        cfg.read('trackers', filepath=args.trackers_file, ignore_missing=True)
        cfg.read('clients', filepath=args.clients_file, ignore_missing=True)
    except errors.ConfigError as e:
        print(e, file=sys.stderr)
        return 1

    # Run UI
    try:
        ui = UI()
        cmd = args.subcmd(args=args, config=cfg)
        assert isinstance(cmd, CommandBase)
        exit_code = ui.run(cmd.jobs_active)

    # TUI was terminated by user prematurely
    except errors.CancelledError as e:
        print(e, file=sys.stderr)
        return 1

    except BaseException as e:
        # Unexpected exception; expected exceptions are handled by JobBase child
        # classes by calling their error() or exception() methods.
        import traceback
        traceback.print_exception(type(e), e, e.__traceback__)
        print()

        # Exceptions from subprocesses should save their traceback.
        # See errors.SubprocessError.
        if hasattr(e, 'original_traceback'):
            print(e.original_traceback)
            print()

        print(f'Please report the traceback above as a bug: {__homepage__}', file=sys.stderr)
        return 1

    else:
        # Print last job's output to stdout
        if exit_code == 0:
            final_job = cmd.jobs_active[-1]
            if final_job.output:
                print('\n'.join(final_job.output))

        return exit_code
