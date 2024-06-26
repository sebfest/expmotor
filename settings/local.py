import os

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    """Get the environment variable or return exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f'Set the {var_name} environment, variable'
        raise ImproperlyConfigured(error_msg)


DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY')
INTERNAL_IPS = ['127.0.0.1', '0.0.0.0']
ALLOWED_HOSTS = INTERNAL_IPS


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
    'django_createsuperuserwithpassword',
    'debug_toolbar',
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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda _request: DEBUG
}

AUTH_USER_MODEL = 'auth.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Oslo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Registration settings
ACCOUNT_ACTIVATION_DAYS = 3
ADMINS = [('admin', 'admin@expmotor.no')]
INCLUDE_REGISTER_URL = False
INCLUDE_AUTH_URLS = True
LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login'
REGISTRATION_OPEN = True
REGISTRATION_DEFAULT_FROM_EMAIL = 'admin@expmotor.no'
REGISTRATION_ADMINS = ADMINS

# Django Sites
SITE_ID = 1

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'DEBUG',
        'handlers': [
            'console'
        ]
    },
    'formatters': {
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'info.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'simple',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
    },
    'loggers': {
        'django': {
            'handlers': [
                'console',
                'file'
            ],
            'level': 'INFO',
            'propagate': True,
        },
        'django.server': {
            'handlers': [
                'django.server',
                'file'
            ],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
