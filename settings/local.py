from settings.base import *

DEBUG = True
ALLOWED_HOSTS = []
INTERNAL_IPS = ['127.0.0.1']
SECRET_KEY = get_env_variable('DB_SECRET_KEY')
POSTGRES_PW = get_env_variable('POSTGRES_PW')
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'messages')
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'expmotor',
        'USER': 'admin',
        'PASSWORD': POSTGRES_PW,
        'HOST': 'localhost',
        'PORT': '',
    }
}