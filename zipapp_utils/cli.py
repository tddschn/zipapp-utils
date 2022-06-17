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


def print_or_write_content(args: argparse.Namespace, output: str):
    if args.out:
        args.out.write_text(output)
    else:
        print(output)


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='zipapp utilities',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument('--pyz', help='Path to the pyz file', type=Path)
    parser.add_argument(
        '-o', '--out', help='Path to the output file, or stdout if not set', type=Path
    )

    return parser.parse_args()


def main():

    args = get_args()
    if args.pyz:
        # shellscript_content = shellscript_bundle_and_run_pyz.format(
        #     encode_file(args.pyz)
        # )
        bundle_and_run_pyz_template_path = Path(__file__).parent / "templates" / "bundle_and_run_pyz.jinja.sh"
        data = {'encoded_pyz_file': encode_file(args.pyz)}
        shellscript_content = render(bundle_and_run_pyz_template_path, data)
        output = shellscript_content.strip()
        print_or_write_content(args, output)
    else:
        print('No pyz file specified')


if __name__ == '__main__':
    main()
