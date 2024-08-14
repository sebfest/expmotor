import os

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    """Get the environment variable or return exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f'Set the {var_name} environment, variable'
        raise ImproperlyConfigured(error_msg)


DEBUG = False
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = get_env_variable('DJANGO_ALLOWED_HOSTS').split(' ')

INSTALLED_APPS = [
    'experiment.apps.ExperimentConfig',
    'account.apps.AccountConfig',
    'registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'bootstrap4',
    'bootstrap_datepicker_plus',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'apps', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'settings.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_variable('POSTGRES_NAME'),
        'USER': get_env_variable('POSTGRES_USER'),
        'PASSWORD': get_env_variable('POSTGRES_PASSWORD'),
        'HOST': get_env_variable('POSTGRES_HOST'),
        'PORT': get_env_variable('POSTGRES_PORT'),
    }
}

AUTH_USER_MODEL = 'auth.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Language
LANGUAGE_CODE = 'en-us'

# Time
TIME_ZONE = 'Europe/Oslo'
USE_I18N = True
USE_TZ = True

# SSL
SECURE_SSL_REDIRECT = True

# Static
WHITENOISE_STATIC_PREFIX = '/static/'
STATIC_URL = '/expmotor/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Media
MEDIA_URL = '/expmotor/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = get_env_variable('EMAIL_HOST')
EMAIL_PORT = get_env_variable('EMAIL_PORT')
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
EMAIL_SUBJECT_PREFIX = ''
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

# Registration settings
ACCOUNT_ACTIVATION_DAYS = 3
ADMINS = [('admin', EMAIL_HOST_USER)]
INCLUDE_REGISTER_URL = False
INCLUDE_AUTH_URLS = True
LOGIN_URL = '/expmotor/accounts/login'
LOGIN_REDIRECT_URL = '/expmotor'
LOGOUT_REDIRECT_URL = '/expmotor/accounts/login'
REGISTRATION_OPEN = True
REGISTRATION_DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
REGISTRATION_ADMINS = ADMINS

# Sites
SITE_ID = 1

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
        },
        'console_on_not_debug': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': [
                'console',
                'mail_admins',
                'console_on_not_debug',
            ],
            'level': 'INFO',
        },
    }
}
