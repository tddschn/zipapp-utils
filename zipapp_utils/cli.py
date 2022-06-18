#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2022-06-17
Purpose: zipapp utilities
"""

import argparse
from . import __version__, __description__, __app_name__, parsers_util


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
    for func in parsers_util.create_parser_functions:
        # print(func.__name__)
        func(subparsers)
    return parser, parser.parse_args()


def main() -> None:
    parser, args = get_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
