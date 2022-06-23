#!/usr/bin/env python3

import argparse
from argparse import ArgumentParser, _SubParsersAction
from pathlib import Path
from .config import DEFAULT_PYTHON3_SHEBANG_ZIPAPP
from .arg_handlers import (
    main_py2pyz,
    main_create_shell_script,
    main_create_archive,
    main_poetry2pyz,
    main_pip2pyz,
)


def create_subparser_create_archive(
    subparsers: _SubParsersAction,
) -> ArgumentParser:
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
        type=Path,
        help="The name of the output archive. " "Required if SOURCE is an archive.",
    )
    subparser_create_archive.add_argument(
        '--python',
        '-p',
        # default=None,
        default=DEFAULT_PYTHON3_SHEBANG_ZIPAPP,
        help="The name of the Python interpreter to use "
        f"(default: {DEFAULT_PYTHON3_SHEBANG_ZIPAPP!r}).",
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
        'source', help="Source directory (or existing archive).", type=Path
    )

    subparser_create_archive.add_argument(
        '--include',
        help="don't exclude files matching PATTERN",
        action='append',
        default=[],
        metavar='PATTERN',
    )

    subparser_create_archive.add_argument(
        '--include-from',
        help='read include patterns from FILE',
        action='append',
        default=[],
        metavar='FILE',
        type=Path,
    )

    subparser_create_archive.add_argument(
        '--exclude',
        help="exclude files matching PATTERN",
        action='append',
        default=[],
        metavar='PATTERN',
    )

    subparser_create_archive.add_argument(
        '--exclude-from',
        help='read exclude patterns from FILE',
        action='append',
        default=[],
        metavar='FILE',
        type=Path,
    )

    subparser_create_archive.add_argument(
        '--dry-run',
        '-n',
        help='perform a trial run with no changes made',
        action='store_true',
    )

    subparser_create_archive.add_argument(
        '--verbose', '-v', help='increase verbosity', action='store_true'
    )
    subparser_create_archive.set_defaults(func=main_create_archive)
    return subparser_create_archive


def create_subparser_py2pyz(
    subparsers: _SubParsersAction,
) -> ArgumentParser:
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
        default=None,
        type=Path,
        # default=argparse.SUPPRESS,
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
    return subparser_py2pyz


def create_subparser_create_shell_script(
    subparsers: _SubParsersAction,
) -> ArgumentParser:

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
        help='Path to the output file',
        type=Path,
    )

    subparser_create_shell_script.set_defaults(func=main_create_shell_script)
    return subparser_create_shell_script


def create_subparser_poetry2pyz(
    subparsers: _SubParsersAction,
) -> ArgumentParser:

    # --------------------
    # subparser_poetry2pyz
    # --------------------
    subparser_poetry2pyz = subparsers.add_parser(
        'poetry2pyz',
        aliases=['poe'],
        help='Create a zipapp archive from a poetry project',
        description='Create a zipapp archive from a poetry project',
    )

    subparser_poetry2pyz.add_argument(
        'poetry_project',
        type=Path,
        help='Path to the poetry project',
        metavar='POETRY_PROJECT',
    )

    subparser_poetry2pyz.add_argument(
        '-o',
        '--output',
        help='Path to the output file',
        type=Path,
    )

    subparser_poetry2pyz.add_argument(
        '-b',
        '--bin',
        help='Entry point name (name of the command)',
        type=str,
    )

    subparser_poetry2pyz.set_defaults(func=main_poetry2pyz)
    return subparser_poetry2pyz


def create_subparser_pip2pyz(
    subparsers: _SubParsersAction,
) -> ArgumentParser:

    # --------------------
    # subparser_pip2pyz
    # --------------------
    subparser_pip2pyz = subparsers.add_parser(
        'pip2pyz',
        aliases=['pip'],
        help='Create a zipapp archive from a pip package',
        description='Create a zipapp archive from a pip package',
    )

    subparser_pip2pyz.add_argument(
        'pip_package',
        type=str,
        help='Name of the pip package',
        metavar='PIP_PACKAGE',
    )

    subparser_pip2pyz.add_argument(
        '-o',
        '--output',
        help='Path to the output file',
        type=Path,
    )

    subparser_pip2pyz.add_argument(
        '-b',
        '--bin',
        help='Entry point name (name of the command)',
        type=str,
    )

    subparser_pip2pyz.set_defaults(func=main_pip2pyz)
    return subparser_pip2pyz


create_parser_functions = [
    create_subparser_create_archive,
    create_subparser_py2pyz,
    create_subparser_create_shell_script,
    create_subparser_poetry2pyz,
    create_subparser_pip2pyz,
]
