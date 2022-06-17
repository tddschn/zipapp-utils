#!/usr/bin/env python3

shellscript_bundle_and_run_pyz = """
#!/usr/bin/env bash

ENCODED_PYZ_FILE='{}'

echo -n "$ENCODED_PYZ_FILE" | base64 -d > /tmp/pyz.pyz
python3 /tmp/pyz.pyz

"""
