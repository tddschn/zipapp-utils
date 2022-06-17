#!/usr/bin/env python3

from pathlib import Path


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
