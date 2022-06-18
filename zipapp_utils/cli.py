#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2022-06-17
Purpose: zipapp utilities
"""

import argparse
from pathlib import Path
from . import __version__, __description__, __app_name__
from .config import DEFAULT_PYTHON3_SHEBANG_ZIPAPP
from .arg_handlers import main_py2pyz, main_create_shell_script, main_create_archive


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        prog=__app_name__,
        description=__description__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version=f'%(prog)s {__version__}',
    )

    subparsers = parser.add_subparsers()
    # --------------------
    # subparser_py2pyz
    # --------------------
    subparser_py2pyz = subparsers.add_parser(
        'py2pyz',
        aliases=['p'],
        help='Create archive from a python script',
        description='Create archive from a python script',
    )

    subparser_py2pyz.add_argument(
        'source', help='Python script file', metavar='SCRIPT', type=Path
    )
    subparser_py2pyz.add_argument(
        '-d', '--dep', help='Add dependency', action='append', default=[]
    )
    subparser_py2pyz.add_argument(
        '-r',
        '--requirement',
        help='Install dependencies from the given requirements file. Defaults to "requirements.txt"',
        type=Path,
        # default=Path('requirements.txt'),
        default=argparse.SUPPRESS,
        nargs='?',
    )
    subparser_py2pyz.add_argument(
        '--output',
        '-o',
        # default=None,
        default=argparse.SUPPRESS,
        help="The name of the output archive. " "Required if SOURCE is an archive.",
    )

    subparser_py2pyz.add_argument(
        '--python',
        '-p',
        # default=None,
        default=DEFAULT_PYTHON3_SHEBANG_ZIPAPP,
        help="The name of the Python interpreter to use " "(default: no shebang line).",
    )
    subparser_py2pyz.add_argument(
        '--main',
        '-m',
        default=None,
        help="The main function of the application "
        "(default: use an existing __main__.py).",
    )
    subparser_py2pyz.add_argument(
        '--compress',
        '-c',
        action='store_true',
        help="Compress files with the deflate method. "
        "Files are stored uncompressed by default.",
    )
    subparser_py2pyz.set_defaults(func=main_py2pyz)
    # --------------------
    # subparser_create_archive
    # --------------------

    subparser_create_archive = subparsers.add_parser(
        'create-archive',
        aliases=['ca', 'zipapp'],
        help='Create a zipapp archive',
        description='Create a zipapp archive',
    )

    # copied from zipapp.py from cpython source
    subparser_create_archive.add_argument(
        '--output',
        '-o',
        default=None,
        help="The name of the output archive. " "Required if SOURCE is an archive.",
    )
    subparser_create_archive.add_argument(
        '--python',
        '-p',
        # default=None,
        default=DEFAULT_PYTHON3_SHEBANG_ZIPAPP,
        help="The name of the Python interpreter to use " "(default: no shebang line).",
    )
    subparser_create_archive.add_argument(
        '--main',
        '-m',
        default=None,
        help="The main function of the application "
        "(default: use an existing __main__.py).",
    )
    subparser_create_archive.add_argument(
        '--compress',
        '-c',
        action='store_true',
        help="Compress files with the deflate method. "
        "Files are stored uncompressed by default.",
    )
    subparser_create_archive.add_argument(
        '--info',
        default=False,
        action='store_true',
        help="Display the interpreter from the archive.",
    )
    subparser_create_archive.add_argument(
        'source', help="Source directory (or existing archive)."
    )

    # --------------------
    # subparser_create_shell_script
    # --------------------

    subparser_create_shell_script = subparsers.add_parser(
        'create-shell-script',
        aliases=['sh'],
        help='Create an ASCII shellscript that runs a zipapp archive',
        description='Create an ASCII shellscript that runs a zipapp archive',
    )

    subparser_create_shell_script.add_argument(
        'pyz',
        help='Path to the pyz file',
        type=Path,
        metavar='PYTHON_APPLICATION_ARCHIVE',
    )
    subparser_create_shell_script.add_argument(
        '-o',
        '--output',
        help='Path to the output file, or stdout if not set',
        type=Path,
    )

    subparser_create_shell_script.set_defaults(func=main_create_shell_script)

    return parser.parse_args()


def main() -> None:
    args = get_args()
    args.func(args)


if __name__ == '__main__':
    main()
