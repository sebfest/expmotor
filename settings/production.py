import dj_database_url

from settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['expmotor.herokuapp.com', '*']

# Database configuration
url = dj_database_url.config(default='postgres://...')
DATABASES['default'].update(url)

# Staticfile collection
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
EMAIL_SUBJECT_PREFIX = ''
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

#SSL
SECURE_SSL_REDIRECT = True







