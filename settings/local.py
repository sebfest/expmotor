from settings.base import *

DEBUG = True
ALLOWED_HOSTS = []
INTERNAL_IPS = ['127.0.0.1']
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'messages')
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
