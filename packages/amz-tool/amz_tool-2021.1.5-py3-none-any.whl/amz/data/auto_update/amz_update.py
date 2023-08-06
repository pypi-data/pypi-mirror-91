#!/usr/bin/env python3

import json
import os
import sys
import subprocess as sp
from urllib.request import urlopen
from packaging.version import parse as ver_parse

import amz.meta as meta
import amz.init as init

# Declare AMZ Data dir
AMZ_DATA_DIR = os.environ['HOME'] + '/.amz/data'

# Check if amz package is updateable
# Get current version
amz_current = meta.get_version()

# Get latest version available
amz_latest_data = json.load(urlopen('https://pypi.org/pypi/amz-tool/json'))
amz_latest = amz_latest_data['info']['version']

if ver_parse(amz_current) < ver_parse(amz_latest):
    # Upgrade via pip
    p = sp.run('python3 -m pip install -U amz-tool', shell=True)
    if p.returncode != 0:
        sys.exit(p.returncode)

    # run init stuff
    if init.amz_update_init():
        sys.exit(0)
