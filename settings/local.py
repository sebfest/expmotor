from settings.base import *

DEBUG = True
INTERNAL_IPS = ['127.0.0.1']
ALLOWED_HOSTS = INTERNAL_IPS

# Email configuration to write on disk
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'messages')

# Debug toolbar
INSTALLED_APPS += ['debug_toolbar']

# Debug toolbar middleware
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
