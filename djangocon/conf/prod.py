import os
from djangocon.conf.global_settings import *

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = os.path.join(PROJECT_DIR, '..', 'djangocon.db')
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

SERVE_STATIC_FILES = False
DEBUG = False

# yeah, this is required by the deployment platform
STATIC_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_DIR, '..', 'static')
MEDIA_URL = '/media/uploads/' # uploads is a symlink to the MEDIA_ROOT dir
ADMIN_MEDIA_PREFIX = '/media/admin/' # collected by staticfiles
