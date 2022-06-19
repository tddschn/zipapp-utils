#!/usr/bin/env python3

from pathlib import Path
from .utils import create_main_py, encode_file, render, print_or_write_content


def create_archive(
    source: Path,
    output: Path | None = None,
    python: str | None = None,
    main: str | None = None,
    compress: bool = False,
    **kwargs,
) -> Path:

    # copied from zipapp.py from cpython source
    # Handle `python -m zipapp archive.pyz --info`.
    source = source.resolve()
    output = output.resolve() if output is not None else source.with_suffix('.pyz')
    import os
    from zipapp import create_archive

    if os.path.isfile(source):
        if output is None or (
            os.path.exists(output) and os.path.samefile(source, output)
        ):
            raise SystemExit("In-place editing of archives is not supported")
        if main:
            raise SystemExit("Cannot change the main function when copying")

    def do_create_archive():
        create_archive(
            source,
            output,
            interpreter=python,
            main=main,
            compressed=compress,
        )

    do_create_archive()
    return output

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


def create_shell_script(
    pyz: Path,
    output: Path | None = None,
    **kwargs,
) -> Path:
    pyz = pyz.resolve()
    bundle_and_run_pyz_template_path = (
        Path(__file__).parent / "templates" / "bundle_and_run_pyz.jinja.sh"
    )
    data = {'encoded_pyz_file': encode_file(pyz)}
    shellscript_content = render(bundle_and_run_pyz_template_path, data)
    output_content = shellscript_content.strip()
    if output is None:
        output = pyz.with_suffix('.sh')
    print_or_write_content(output_content, output, True)
    return output


def py2pyz(
    source: Path,
    dep: list[str] = [],
    use_requirements_txt: bool = False,
    requirement: Path | None = None,
    output: Path | None = None,
    python: str | None = None,
    main: str | None = None,
    compress: bool = False,
    **kwargs,
) -> Path:
    source = source.resolve()
    source_parent_dir = str(source.parent)
    if use_requirements_txt:
        if requirement is None:
            requirement = source.with_name('requirements.txt')
        if not requirement.exists():
            raise SystemExit(f'Requirements file {str(requirement)} does not exist')
        from pip._internal.utils.entrypoints import _wrapper

        _wrapper(['install', '-r', str(requirement), '--target', source_parent_dir])
    if dep:
        from pip._internal.utils.entrypoints import _wrapper

        _wrapper(['install', '-U'] + dep + ['--target', source_parent_dir])

    for dist_info_dir in Path(source_parent_dir).glob('*.dist-info'):
        # rm -rf *.dist-info
        from shutil import rmtree

        rmtree(dist_info_dir)

    has_main = (source / '__main__.py').is_file()
    if not has_main:
        # creates __main__.py if it doesn't exist
        create_main_py(source, main)

    # if 'output' not in args:
    #     output = source.with_suffix('.pyz')
    # if you do this, you'll add the pyz file in that dir and increase the dir size, and might cause issues if you zip that dir

    from zipapp import create_archive

    create_archive(
        source_parent_dir,
        output,
        interpreter=python,
        main=main,
        compressed=compress,
    )
    return source.with_suffix('.pyz') if output is None else output


def poetry2pyz(
    poetry_project: Path, output: Path | None = None, bin: str | None = None, **kwargs
) -> Path:
    poetry_project = poetry_project.resolve()
    return poetry_project.with_suffix('.pyz') if output is None else output


def pip2pyz(
    pip_package: str, output: Path | None = None, bin: str | None = None, **kwargs
) -> Path:
    from pip._internal.utils.entrypoints import _wrapper

    # make a secure temp dir
    from tempfile import TemporaryDirectory

    tempdir = TemporaryDirectory()
    tempdir_path = Path(tempdir.name)
    _wrapper(['install', pip_package, '--target', str(tempdir_path)])
    return (
        Path(f'./{pip_package}').resolve().with_suffix('.pyz')
        if output is None
        else output
    )
