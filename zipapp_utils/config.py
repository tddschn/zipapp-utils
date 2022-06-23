#!/usr/bin/env python3

from .filters import null_filter

DEFAULT_PYTHON3_SHEBANG_ZIPAPP = '/usr/bin/env python3'
# DEFAULT_ZIPAPP_FILTER = exclude_dist_info_and_pyz
DEFAULT_ZIPAPP_FILTER = null_filter

FILTER_ARGS = ['--include', '--include-from', '--exclude', '--exclude-from']
