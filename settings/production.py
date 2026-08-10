import os

from django.core.exceptions import ImproperlyConfigured

from .base import *


def get_env_variable(var_name):
    """Get an environment variable or raise a useful configuration error."""
    try:
        return os.environ[var_name]
    except KeyError as exc:
        raise ImproperlyConfigured(f"Set the {var_name} environment variable") from exc


DEBUG = False
SECRET_KEY = get_env_variable("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = get_env_variable("DJANGO_ALLOWED_HOSTS").split()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_env_variable("POSTGRES_NAME"),
        "USER": get_env_variable("POSTGRES_USER"),
        "PASSWORD": get_env_variable("POSTGRES_PASSWORD"),
        "HOST": get_env_variable("POSTGRES_HOST"),
        "PORT": get_env_variable("POSTGRES_PORT"),
    }
}

STATIC_URL = "/expmotor/static/"
MEDIA_URL = "/expmotor/media/"
WHITENOISE_STATIC_PREFIX = "/static/"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = get_env_variable("EMAIL_HOST")
EMAIL_PORT = int(get_env_variable("EMAIL_PORT"))
EMAIL_HOST_USER = get_env_variable("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_env_variable("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

ADMINS = [("admin", EMAIL_HOST_USER)]
LOGIN_URL = "/expmotor/accounts/login"
LOGIN_REDIRECT_URL = "/expmotor"
LOGOUT_REDIRECT_URL = "/expmotor/accounts/login"
REGISTRATION_DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
REGISTRATION_ADMINS = ADMINS

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
CSRF_TRUSTED_ORIGINS = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split()

CELERY_BROKER_URL = get_env_variable("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = get_env_variable("CELERY_RESULT_BACKEND")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "filters": ["require_debug_false"],
        },
        "mail_admins": {
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],
            "level": "ERROR",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
        },
    },
}
