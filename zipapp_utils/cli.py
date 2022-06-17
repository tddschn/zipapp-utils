#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2022-06-17
Purpose: zipapp utilities
"""

import argparse
from pathlib import Path
from shutil import rmtree
from .utils import create_main_py, encode_file, render
from .config import DEFAULT_PYTHON3_SHEBANG_ZIPAPP

# from .templates import shellscript_bundle_and_run_pyz


def print_or_write_content(
    args: argparse.Namespace, output: str, make_executable: bool = False
) -> None:
    if args.output:
        args.output.write_text(output)
        if make_executable:
            st = args.output.stat()
            args.output.chmod(st.st_mode | 0o0100)
    else:
        print(output)


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='zipapp utilities',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
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
        help='create a zipapp archive',
        description='create a zipapp archive',
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
        help='create an ASCII shellscript that runs a zipapp archive',
        description='create an ASCII shellscript that runs a zipapp archive',
    )

    subparser_create_shell_script.add_argument(
        '--pyz', help='Path to the pyz file', type=Path
    )
    subparser_create_shell_script.add_argument(
        '-o',
        '--output',
        help='Path to the output file, or stdout if not set',
        type=Path,
    )

    subparser_create_shell_script.set_defaults(func=main_create_shell_script)

    return parser.parse_args()


def main_create_archive(args: argparse.Namespace):
    # copied from zipapp.py from cpython source
    # Handle `python -m zipapp archive.pyz --info`.
    import os
    import sys
    from zipapp import create_archive, get_interpreter

    if args.info:
        if not os.path.isfile(args.source):
            raise SystemExit("Can only get info for an archive file")
        interpreter = get_interpreter(args.source)
        print("Interpreter: {}".format(interpreter or "<none>"))
        sys.exit(0)

    if os.path.isfile(args.source):
        if args.output is None or (
            os.path.exists(args.output) and os.path.samefile(args.source, args.output)
        ):
            raise SystemExit("In-place editing of archives is not supported")
        if args.main:
            raise SystemExit("Cannot change the main function when copying")

    def do_create_archive():
        create_archive(
            args.source,
            args.output,
            interpreter=args.python,
            main=args.main,
            compressed=args.compress,
        )

    do_create_archive()
    print(f'Created {str(args.output)}')

    # try:
    #     do_create_archive()
    # except ZipAppError as e:
    #     # main = args.main  # like myapp.cli:main
    #     # source = Path(args.source)
    #     # if not source.exists():
    #     #     raise e
    #     # has_main = (source / '__main__.py').is_file()
    #     # if not (not main != (not has_main)):
    #     #     # xor, see https://stackoverflow.com/a/35198876/11133602
    #     #     raise e
    #     # if not has_main:
    #     #     create_main_py(main)
    #     raise e


def main_create_shell_script(args: argparse.Namespace):

    # args = get_args()
    if args.pyz:
        # shellscript_content = shellscript_bundle_and_run_pyz.format(
        #     encode_file(args.pyz)
        # )
        bundle_and_run_pyz_template_path = (
            Path(__file__).parent / "templates" / "bundle_and_run_pyz.jinja.sh"
        )
        data = {'encoded_pyz_file': encode_file(args.pyz)}
        shellscript_content = render(bundle_and_run_pyz_template_path, data)
        output = shellscript_content.strip()
        print_or_write_content(args, output, True)
    else:
        print('No pyz file specified')


def main_py2pyz(args: argparse.Namespace):
    source_parent_dir = str(args.source.parent)
    if 'requirement' in args:
        if args.requirement is None:
            args.requirement = args.source.with_name('requirements.txt')
        if not args.requirement.exists():
            raise SystemExit(
                f'Requirements file {str(args.requirement)} does not exist'
            )
        from pip._internal.utils.entrypoints import _wrapper

        _wrapper(
            ['install', '-r', str(args.requirement), '--target', source_parent_dir]
        )
    if args.dep:
        from pip._internal.utils.entrypoints import _wrapper

        _wrapper(['install', '-U'] + args.dep + ['--target', source_parent_dir])

    for dist_info_dir in Path(source_parent_dir).glob('*.dist-info'):
        # rm -rf *.dist-info
        rmtree(dist_info_dir)

    has_main = (args.source / '__main__.py').is_file()
    if not has_main:
        # creates __main__.py if it doesn't exist
        create_main_py(args.source, args.main)

    if 'output' not in args:
        args.output = args.source.with_suffix('.pyz')

    from zipapp import create_archive

    create_archive(
        source_parent_dir,
        args.output,
        interpreter=args.python,
        main=args.main,
        compressed=args.compress,
    )

    print(f'Created {str(args.output)}')


def main() -> None:
    args = get_args()
    args.func(args)


if __name__ == '__main__':
    main()
