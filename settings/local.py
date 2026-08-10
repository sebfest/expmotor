import os
import sys

from .base import *


def get_env_variable(var_name):
    """Get an environment variable or raise a useful configuration error."""
    from django.core.exceptions import ImproperlyConfigured

    try:
        return os.environ[var_name]
    except KeyError as exc:
        raise ImproperlyConfigured(f"Set the {var_name} environment variable") from exc


DEBUG = True
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost 127.0.0.1").split()
INTERNAL_IPS = ALLOWED_HOSTS

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

INSTALLED_APPS += ["django_createsuperuserwithpassword"]
ENABLE_DEBUG_TOOLBAR = DEBUG and "test" not in sys.argv
if ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda _request: DEBUG}

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

ADMINS = [("admin", "admin@expmotor.no")]
LOGIN_URL = "/accounts/login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login"
REGISTRATION_DEFAULT_FROM_EMAIL = "admin@expmotor.no"
REGISTRATION_ADMINS = ADMINS

CELERY_BROKER_URL = get_env_variable("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = get_env_variable("CELERY_RESULT_BACKEND")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "{levelname} {asctime} {message}", "style": "{"},
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple"},
        "django.server": {
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
