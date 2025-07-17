#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

# Project root directory
BASE_PATH = Path(__file__).resolve().parent.parent

# Alembic migration files directory
ALEMBIC_VERSION_DIR = BASE_PATH / 'alembic' / 'versions'

# Log files directory
LOG_DIR = BASE_PATH / 'log'

# Static resources directory
STATIC_DIR = BASE_PATH / 'static'

# Upload files directory
UPLOAD_DIR = STATIC_DIR / 'upload'

# Plugin directory
PLUGIN_DIR = BASE_PATH / 'plugin'

# Offline IP database path
IP2REGION_XDB = STATIC_DIR / 'ip2region.xdb'
