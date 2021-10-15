from settings.base import *

DEBUG = True
INTERNAL_IPS = ['127.0.0.1']
ALLOWED_HOSTS = INTERNAL_IPS
SECRET_KEY = get_env_variable('DB_SECRET_KEY')

# Email configuration to write on disk
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'messages')

# Debug toolbar
INSTALLED_APPS += ['debug_toolbar']

# Debug toolbar middleware
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

# POSTGRES
POSTGRES_PW = get_env_variable('POSTGRES_PW')
DATABASES['default'].update(
    {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'expmotor',
        'USER': 'admin',
        'PASSWORD': POSTGRES_PW,
        'HOST': 'localhost',
        'PORT': '',
    }
)
