from config.base import *

conn_info = fetch_connections_info()

CORS_ENABLED = True

SQLALCHEMY_LOG_LEVEL = logging.INFO
ALEMBIC_PRINT_SQL = True
DEBUG = True


# SQLALCHEMY/ALEMBIC Settings
SQLALCHEMY_DATABASE_URI = ''.join(['postgresql://',
                                   conn_info["RDBMS"]["CLIENT_ID"], ':', conn_info["RDBMS"]["CLIENT_SECRET"],
                                   '@ithriv_db', ':', conn_info["RDBMS"]["PORT"],
                                   ''.join(['/ithriv-', conn_info['ENV']])])

# Amazon S3 Bucket for storing images.

# Elastic Search Settings
ELASTIC_SEARCH['hosts'] = ["ithriv_es"]

# SMTP Email Settings
MAIL_SERVER = 'postfix'
# Single Signon configuration Settings
SSO_ATTRIBUTE_MAP['uid'] = (False, 'uid')
SSO_DEVELOPMENT_EPPN = 'ithriv_admin@virginia.edu'
MAIL_CONSULT_RECIPIENT = 'rkc7h@virginia.edu'

API_URL = 'http://localhost'
SITE_URL = 'http://localhost'
FRONTEND_AUTH_CALLBACK, FRONTEND_EMAIL_RESET, FRONTEND_EMAIL_CONFIRM = auth_callback_url_tuple(
    SITE_URL, '/#/session', '/#/reset_password/', '/#/login/')
