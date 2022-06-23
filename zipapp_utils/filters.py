#!/usr/bin/env python3
"""Filter functions for zipapp.create_archive"""


from pathlib import Path
from collections.abc import Callable, Iterable


def null_filter(path: Path) -> bool:
    return True


def exclude_dist_info(path: Path) -> bool:
    return path.suffix != '.dist-info'


def exclude_pyz(path: Path) -> bool:
    return path.suffix != '.pyz'


def exclude_dist_info_and_pyz(path: Path) -> bool:
    return exclude_dist_info(path) and exclude_pyz(path)


def create_pattern_set(
    patterns: Iterable[str], pattern_from: Iterable[Path]
) -> set[str]:
    patterns = set(patterns)
    pattern_from = set(pattern_from)
    patterns_set = patterns.copy()
    for pattern_file in pattern_from:
        patterns.update(pattern_file.read_text().splitlines())
    return patterns_set


def make_filter_function(
    base_dir: Path, include_patterns: Iterable[str], exclude_patterns: Iterable[str]
) -> Callable[[Path], bool]:
    """Create a filter function from include and exclude patterns.
    exclude glob patterns from exclude_patterns, except those in the include_patterns"""
    base_dir = base_dir.resolve()
    include_patterns = set(include_patterns)
    exclude_patterns = set(exclude_patterns)
    # all_files: all files in base_dir, recursive, including hidden files
    all_files = set(base_dir.rglob('*.?*'))
    excluded_files = set()
    for pattern in exclude_patterns:
        excluded_files.update(base_dir.glob(pattern))
    included_files = set()
    for pattern in include_patterns:
        included_files.update(base_dir.glob(pattern))
    net_excluded_files = excluded_files - included_files
    all_files_included = all_files - net_excluded_files

    def filter_function(path: Path) -> bool:
        if path.resolve() in all_files_included:
            return True
        return False

    return filter_function


def make_filter_function_from_args(
    base_dir: Path,
    include: Iterable[str],
    include_from: Iterable[Path],
    exclude: Iterable[str],
    exclude_from: Iterable[Path],
    **kwargs
) -> Callable[[Path], bool]:
    include_set = create_pattern_set(include, include_from)
    exclude_set = create_pattern_set(exclude, exclude_from)
    return make_filter_function(base_dir, include_set, exclude_set)
