import argparse

from .api import py2pyz, create_archive_zau, create_shell_script, poetry2pyz, pip2pyz
from .config import DEFAULT_ZIPAPP_FILTER


def main_create_archive(args: argparse.Namespace):
    if args.info:
        from zipapp import get_interpreter
        import os, sys

        if not os.path.isfile(args.source):
            raise SystemExit("Can only get info for an archive file")
        interpreter = get_interpreter(args.source)
        print("Interpreter: {}".format(interpreter or "<none>"))
        sys.exit(0)

    output = create_archive_zau(**vars(args), filter=DEFAULT_ZIPAPP_FILTER)
    print(f'Created {str(output)}')


def main_py2pyz(args: argparse.Namespace):
    if hasattr(args, 'requirement'):
        args.use_requirements_txt = True
    output = py2pyz(**vars(args), filter=DEFAULT_ZIPAPP_FILTER)
    print(f'Created {str(output)}')


def main_create_shell_script(args: argparse.Namespace):
    output = create_shell_script(**vars(args), filter=DEFAULT_ZIPAPP_FILTER)
    print(f'Created {str(output)}')


def main_poetry2pyz(args: argparse.Namespace):
    output = poetry2pyz(**vars(args), filter=DEFAULT_ZIPAPP_FILTER)
    print(f'Created {str(output)}')


def main_pip2pyz(args: argparse.Namespace):
    output = pip2pyz(**vars(args), filter=DEFAULT_ZIPAPP_FILTER)
    print(f'Created {str(output)}')
