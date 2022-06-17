#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2022-06-17
Purpose: zipapp utilities
"""

import argparse
from pathlib import Path
from .utils import encode_file, render

# from .templates import shellscript_bundle_and_run_pyz


def print_or_write_content(
    args: argparse.Namespace, output: str, make_executable: bool = False
) -> None:
    if args.out:
        args.out.write_text(output)
        if make_executable:
            st = args.out.stat()
            args.out.chmod(st.st_mode | 0o0100)
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
        default=None,
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
        '-o', '--out', help='Path to the output file, or stdout if not set', type=Path
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

    create_archive(
        args.source,
        args.output,
        interpreter=args.python,
        main=args.main,
        compressed=args.compress,
    )


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


def main() -> None:
    args = get_args()
    args.func(args)


if __name__ == '__main__':
    main()
