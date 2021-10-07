from settings.base import *

DEBUG = False
ALLOWED_HOSTS = []
EMAIL_BACKEND = get_env_variable('EMAIL_BACKEND')
EMAIL_USE_TLS = get_env_variable('EMAIL_USE_TLS')
EMAIL_HOST = get_env_variable('EMAIL_HOST')
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
EMAIL_PORT = get_env_variable('EMAIL_PORT')
DEFAULT_FROM_EMAIL = get_env_variable('EMAIL_HOST_USER')
