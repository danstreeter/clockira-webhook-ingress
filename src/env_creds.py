"""Imports env vars into local variables for import via config.py"""
# noqa

import os

APP_NODE = os.environ.get('APP_NODE', 'development')

API_PREFIX = os.environ.get('API_PREFIX', '')

DEBUG = os.environ.get('WEBHOOK_DEBUG', False)

RABBIT_SERVER = os.environ.get("RABBIT_SERVER", "")
RABBIT_PORT = os.environ.get("RABBIT_PORT", "")
RABBIT_USER = os.environ.get("RABBIT_USER", "")
RABBIT_PASS = os.environ.get("RABBIT_PASS", "")
