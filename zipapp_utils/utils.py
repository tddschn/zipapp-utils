#!/usr/bin/env python3

from pathlib import Path
from logging import Logger
from typing import Callable


def encode_file(file_path: Path) -> str:
    """Encode a file with base64.

    Args:
        file_path: Path to the file to encode.

    Returns:
        The encoded file."""

    from base64 import b64encode

    return b64encode(file_path.read_bytes()).decode()


# --------------------
# force_text and render are
# copied from jinja2cli/cli.py (pypi: jinja2-cli) and modified
# a copy of jinja2-cli's license can be found in the LICENSE.jinja2-cli file
# --------------------


def force_text(data: str | bytes) -> str:
    if isinstance(data, str):
        return data
    if isinstance(data, bytes):
        return data.decode()
    return data


def render(
    template_path: Path,
    data: dict[str, str],
    extensions: list[str] = [],
    strict: bool = False,
) -> str:
    from jinja2 import (
        __version__ as jinja_version,
        Environment,
        FileSystemLoader,
        StrictUndefined,
    )
    import os

    # Starting with jinja2 3.1, `with_` and `autoescape` are no longer
    # able to be imported, but since they were default, let's stub them back
    # in implicitly for older versions.
    # We also don't track any lower bounds on jinja2 as a dependency, so
    # it's not easily safe to know it's included by default either.

    # extensions = [
    #     "do",
    #     "loopcontrols",
    # ] + extensions  # copied from jinja2-cli's main func
    if tuple(jinja_version.split(".", 2)) < ("3", "1"):
        for ext in "with_", "autoescape":
            ext = "jinja2.ext." + ext
            if ext not in extensions:
                extensions.append(ext)

    env = Environment(
        loader=FileSystemLoader(template_path.parent),
        extensions=extensions,
        keep_trailing_newline=True,
    )
    if strict:
        env.undefined = StrictUndefined

    # Add environ global
    env.globals["environ"] = lambda key: force_text(os.environ.get(key, ''))
    env.globals["get_context"] = lambda: data

    return env.get_template(template_path.name).render(data)


# --------------------
# end of copied code
# --------------------


def create_main_py(python_script: Path, entry_point: str | None = None) -> Path:
    """Create a __main__.py file in the same directory."""
    main_py = python_script.parent / "__main__.py"
    if entry_point is not None:
        # Check that main has the right format.
        # copied from zipapp.py from cpython source
        from zipapp import ZipAppError, MAIN_TEMPLATE  # type: ignore

        mod, sep, fn = entry_point.partition(':')
        mod_ok = all(part.isidentifier() for part in mod.split('.'))
        fn_ok = all(part.isidentifier() for part in fn.split('.'))
        if not (sep == ':' and mod_ok and fn_ok):
            raise ZipAppError("Invalid entry point: " + entry_point)
        main_py_content = MAIN_TEMPLATE.format(module=mod, fn=fn)
    else:
        main_py_content = render(
            Path(__file__).parent / "templates" / "__main__.jinja.py",
            {'script_name': python_script.stem},
        )
    main_py.write_text(main_py_content)
    return main_py


def print_or_write_content(
    output_content: str, output: Path | None = None, make_executable: bool = False
) -> None:
    if output:
        output.write_text(output_content)
        if make_executable:
            st = output.stat()
            output.chmod(st.st_mode | 0o0100)
    else:
        print(output)


def create_archive_with_logging(
    logger: Logger,
    source,
    target=None,
    interpreter: str | None = None,
    main=None,
    filter: Callable[[Path], bool] | None = None,
    compressed: bool = False,
):
    """zipapp.create_archive with logging"""
    from zipapp import create_archive

    logger.info(
        f'Running create_archive with args: {source=}, {target=}, {interpreter=}, {main=}, {filter=}, {compressed=}'
    )
    create_archive(
        source=source,
        target=target,
        interpreter=interpreter,
        main=main,
        filter=filter,
        compressed=compressed,
    )
    logger.info(f'create_archive finished')
