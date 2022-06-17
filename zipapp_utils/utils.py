#!/usr/bin/env python3

from base64 import b64encode
from pathlib import Path


def encode_file(file_path: Path) -> str:
    """Encode a file with base64.

    Args:
        file_path: Path to the file to encode.

    Returns:
        The encoded file."""

    return b64encode(file_path.read_bytes()).decode()
