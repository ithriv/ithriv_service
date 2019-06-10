from config.base import *

CORS_ENABLED = True

# SQLALCHEMY/ALEMBIC Settings
SQLALCHEMY_LOG_LEVEL = logging.INFO
ALEMBIC_PRINT_SQL = True

# Amazon S3 Bucket for storing images.

# Elastic Search Settings

# SMTP Email Settings

# Single Signon configuration Settings
SSO_ATTRIBUTE_MAP['uid'] = (False, 'uid')
SSO_DEVELOPMENT_EPPN = 'ithriv_admin@virginia.edu'

API_URL = 'http://uat.ithriv.org'
SITE_URL = 'http://uat.ithriv.org'
FRONTEND_AUTH_CALLBACK, FRONTEND_EMAIL_RESET, FRONTEND_EMAIL_CONFIRM = auth_callback_url_tuple(
    SITE_URL, '/#/session', '/#/reset_password/', '/#/login/')
