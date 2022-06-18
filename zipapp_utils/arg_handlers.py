import argparse

from .api import py2pyz, create_archive, create_shell_script


def main_py2pyz(args: argparse.Namespace):
    output = py2pyz(**vars(args))
    print(f'Created {str(output)}')


def main_create_archive(args: argparse.Namespace):
    if args.info:
        from zipapp import get_interpreter
        import os, sys

        if not os.path.isfile(args.source):
            raise SystemExit("Can only get info for an archive file")
        interpreter = get_interpreter(args.source)
        print("Interpreter: {}".format(interpreter or "<none>"))
        sys.exit(0)

    output = create_archive(**vars(args))
    print(f'Created {str(output)}')


def main_create_shell_script(args: argparse.Namespace):
    output = create_shell_script(**vars(args))
    print(f'Created {str(output)}')
