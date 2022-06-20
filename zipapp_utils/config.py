#!/usr/bin/env python3

from .filters import exclude_dist_info_and_pyz

DEFAULT_PYTHON3_SHEBANG_ZIPAPP = '/usr/bin/env python3'
DEFAULT_ZIPAPP_FILTER = exclude_dist_info_and_pyz
