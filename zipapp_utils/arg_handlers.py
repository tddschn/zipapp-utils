import argparse
from pathlib import Path

from shutil import rmtree
from .utils import create_main_py, encode_file, render, print_or_write_content


def main_py2pyz(args: argparse.Namespace):
    args.source = args.source.resolve()
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

    # if 'output' not in args:
    #     args.output = args.source.with_suffix('.pyz')
    # if you do this, you'll add the pyz file in that dir and increase the dir size, and might cause issues if you zip that dir

    from zipapp import create_archive

    create_archive(
        source_parent_dir,
        args.output,
        interpreter=args.python,
        main=args.main,
        compressed=args.compress,
    )

    print(f'Created {str(args.output)}')


def main_create_archive(args: argparse.Namespace):
    # copied from zipapp.py from cpython source
    # Handle `python -m zipapp archive.pyz --info`.
    import os
    import sys
    from zipapp import create_archive, get_interpreter

    args.source = args.source.resolve()

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

    output = args.output
    if output is None:
        output = args.source.with_suffix('.pyz')

    def do_create_archive():
        create_archive(
            args.source,
            output,
            interpreter=args.python,
            main=args.main,
            compressed=args.compress,
        )

    do_create_archive()
    print(f'Created {str(output)}')

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
    bundle_and_run_pyz_template_path = (
        Path(__file__).parent / "templates" / "bundle_and_run_pyz.jinja.sh"
    )
    data = {'encoded_pyz_file': encode_file(args.pyz)}
    shellscript_content = render(bundle_and_run_pyz_template_path, data)
    output = shellscript_content.strip()
    print_or_write_content(args, output, True)
