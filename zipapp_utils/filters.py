#!/usr/bin/env python3
"""Filter functions for zipapp.create_archive"""


from pathlib import Path


def exclude_dist_info(path: Path) -> bool:
    return path.suffix != '.dist-info'


def exclude_pyz(path: Path) -> bool:
    return path.suffix != '.pyz'


def exclude_dist_info_and_pyz(path: Path) -> bool:
    return exclude_dist_info(path) and exclude_pyz(path)
