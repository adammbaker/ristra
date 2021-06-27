"""
Django settings for ristra project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from socket import gethostname, gethostbyname

# to get around an import NameError
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import SHA256
import environ

env = environ.Env()
env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")
# DEBUG key is also being used to see if this is a development setting

SOFTWARE_CYCLE = env("SOFTWARE_CYCLE")

if SOFTWARE_CYCLE == 'dev':
    ALLOWED_HOSTS = [
        u'192.168.0.151',
        u'localhost',
        u'dev.ristrarefuge.org',
    ]
elif SOFTWARE_CYCLE == 'beta':
    ALLOWED_HOSTS = [
        u'localhost',
        u'beta.ristrarefuge.org',
    ]
elif SOFTWARE_CYCLE == 'prod':
    ALLOWED_HOSTS = [
        u'localhost',
        u'ristrarefuge.org',
        u'www.ristrarefuge.org',
    ]

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition

INSTALLED_APPS = [
    'qr_code',
    'shortener',
    'bootstrap4',
    'simple_history',
    'intake.apps.IntakeConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("DATABASE_NAME"),
        'USER': env("DATABASE_USER"),
        'PASSWORD': env("DATABASE_PASSWORD"),
        'HOST': env("DATABASE_HOST"),
        'PORT': env("DATABASE_PORT"),
        }
}

ROOT_URLCONF = 'ristra.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'ristra.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': f'/tmp/{env("SOFTWARE_CYCLE")}.ristrarefuge.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Denver'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Base url to serve static files
STATIC_URL = '/static/'
# Path where static files are stored
if SOFTWARE_CYCLE == 'dev':
    STATIC_ROOT = os.path.join(BASE_DIR, '/var/www/dev.ristrarefuge.org/static/')
elif SOFTWARE_CYCLE == 'beta':
    STATIC_ROOT = os.path.join(BASE_DIR, '/var/www/beta.ristrarefuge.org/static/')
elif SOFTWARE_CYCLE == 'prod':
    STATIC_ROOT = os.path.join(BASE_DIR, '/var/www/ristrarefuge.org/static/')

# Base url to serve media files
MEDIA_URL = '/media/'
# Path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BOOTSTRAP4 = {
    'include_jquery': True,
}

DATABASE_REGIME = 'postgresql'
if SOFTWARE_CYCLE == 'dev':
    BASE_URL = 'http://localhost:8000'
    BASE_URL = 'https://dev.ristrarefuge.org'
    # BASE_URL = 'http://dev.ristrarefuge.org:8000'
elif SOFTWARE_CYCLE == 'beta':
    BASE_URL = 'http://localhost:8000'
    BASE_URL = 'https://beta.ristrarefuge.org'
    # BASE_URL = 'http://dev.ristrarefuge.org:8000'
elif SOFTWARE_CYCLE == 'prod':
    BASE_URL = 'http://localhost:8000'
    BASE_URL = 'https://www.ristrarefuge.org'
    # BASE_URL = 'http://www.ristrarefuge.org:8000'

SHORTENER_ENABLED = True
SHORTENER_MAX_URLS = -1
SHORTENER_MAX_CONCURRENT = 100 # To prevent spamming
SHORTENER_LIFESPAN = 604800
SHORTENER_MAX_USES = -1
SHORTENER_ENABLE_TEST_PATH = True

# Email info
if SOFTWARE_CYCLE == 'dev':
    DEFAULT_HOST = 'http://dev.ristrarefuge.com'
elif SOFTWARE_CYCLE == 'beta':
    DEFAULT_HOST = 'http://beta.ristrarefuge.com'
elif SOFTWARE_CYCLE == 'prod':
    DEFAULT_HOST = 'http://www.ristrarefuge.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FROM = 'Ristra Refuge Dev <ristrarefuge@gmail.com>'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'ristrarefuge@gmail.com'
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

SECRET_SALT = b'\x8b\x85R\xd9\xc8\xa3\xc4rs2F\xc5\\\x035*'
HASHID_FIELD_SALT = env("HASHID_FIELD_SALT")

# Encryption via django-crpytography
CRYPTOGRAPHY_BACKEND = default_backend()
CRYPTOGRAPHY_DIGEST = SHA256
CRYPTOGRAPHY_KEY = env("CRYPTOGRAPHY_KEY")
