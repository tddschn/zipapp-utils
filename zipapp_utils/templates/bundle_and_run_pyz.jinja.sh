#!/usr/bin/env bash

ENCODED_PYZ_FILE='{{ encoded_pyz_file }}'

echo -n "${ENCODED_PYZ_FILE}" | base64 -d > /tmp/pyz.pyz
python3 /tmp/pyz.pyz
