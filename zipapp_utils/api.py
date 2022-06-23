#!/usr/bin/env python3

from pathlib import Path
from .utils import (
    create_main_py,
    encode_file,
    render,
    print_or_write_content,
    create_archive_with_logging,
)
from . import EntryPointNotFoundError, ProjectNameNotFoundError, logger


def create_archive_zau(
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

    if source.is_file():
        if output is None or (output.exists() and source.samefile(output)):
            raise SystemExit("In-place editing of archives is not supported")
        if main:
            raise SystemExit("Cannot change the main function when copying")

    def do_create_archive():
        create_archive_with_logging(
            logger,
            source,
            output,
            interpreter=python,
            main=main,
            filter=kwargs['filter'] if 'filter' in kwargs else None,
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
    logger.info(f'Creating pyz from {source}')
    logger.info(f'args:')
    logger.info(f'source: {source}')
    logger.info(f'dep: {dep}')
    logger.info(f'use_requirements_txt: {use_requirements_txt}')
    logger.info(f'requirement: {requirement}')
    logger.info(f'output: {output}')
    logger.info(f'python: {python}')
    logger.info(f'main: {main}')
    logger.info(f'compress: {compress}')
    logger.info(f'kwargs: {kwargs}')
    source = source.resolve()
    source_parent_dir = source.parent
    source_parent_dir_s = str(source_parent_dir)
    output = (
        output.resolve()
        if output is not None
        else source_parent_dir.with_suffix('.pyz')
    )
    if use_requirements_txt:
        if requirement is None:
            requirement = source.with_name('requirements.txt')
        if not requirement.exists():
            raise SystemExit(f'Requirements file {str(requirement)} does not exist')
        from pip._internal.utils.entrypoints import _wrapper

        pip_args = ['install', '-r', str(requirement), '--target', source_parent_dir_s]
        logger.info(f'Using requirements file {str(requirement)}')
        logger.info(f'Running pip with args: {pip_args}')
        _wrapper(pip_args)
    if dep:
        from pip._internal.utils.entrypoints import _wrapper

        pip_args = ['install', '-U'] + dep + ['--target', source_parent_dir_s]
        logger.info(f'Running pip with args: {pip_args}')
        _wrapper(pip_args)

    # for dist_info_dir in Path(source_parent_dir_s).glob('*.dist-info'):
    #     # rm -rf *.dist-info
    #     from shutil import rmtree

    #     rmtree(dist_info_dir)

    has_main = (source_parent_dir / '__main__.py').is_file()
    if not has_main:
        # creates __main__.py if it doesn't exist
        main_py = create_main_py(source, main)
        logger.info(f'Created {str(main_py)}')

    # if 'output' not in args:
    #     output = source.with_suffix('.pyz')
    # if you do this, you'll add the pyz file in that dir and increase the dir size, and might cause issues if you zip that dir

    # from zipapp import create_archive

    # create_archive_with_logging(
    #     logger,
    #     source_parent_dir_s,
    #     target=output,
    #     interpreter=python,
    #     main=main,
    #     filter=kwargs['filter'] if 'filter' in kwargs else None,
    #     compressed=compress,
    # )
    # return source.with_suffix('.pyz') if output is None else output

    create_archive_zau(
        source_parent_dir,
        target=output,
        interpreter=python,
        main=main,
        filter=kwargs['filter'] if 'filter' in kwargs else None,
        compressed=compress,
    )


def poetry2pyz(
    poetry_project: Path, output: Path | None = None, bin: str | None = None, **kwargs
) -> Path:
    poetry_project = poetry_project.resolve()
    pyproject_toml_path = poetry_project / 'pyproject.toml'
    from poetry.core.pyproject.toml import PyProjectTOML

    ppt = PyProjectTOML(pyproject_toml_path)
    try:
        all_entry_point_commands = set(ppt.poetry_config['scripts'])  # type: ignore
    except:
        raise EntryPointNotFoundError(
            f'No entry point found in {str(pyproject_toml_path)}'
        )
    if bin is None:
        try:
            project_name = ppt.poetry_config['name']  # type: ignore
            assert project_name != ''
        except:
            raise ProjectNameNotFoundError(
                f'No project name found in {str(pyproject_toml_path)}. It\'s used as the default entry point if --bin is not specified.'
            )
        bin = project_name
    if bin not in all_entry_point_commands:
        raise EntryPointNotFoundError(
            f'No entry point found in {str(pyproject_toml_path)} for {bin}'
        )

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
