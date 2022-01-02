"""
Django settings for community project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hxbpraj5pl@tse*(2k(&d7bc^57d#y(37%$i!13@q^)^3r0cc$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'communityapp-env-1.eba-w26fpz3a.us-east-2.elasticbeanstalk.com',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'events',
    'members',
    'services',
    'rest_framework',
    'django_elasticsearch_dsl',
    'django_elasticsearch_dsl_drf',
    'location_field.apps.DefaultConfig',
    'easy_maps',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'community.urls'

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

WSGI_APPLICATION = 'community.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'community',
        'USER': 'master_user',
        'PASSWORD': 'can_all',
        'HOST': 'swe578_mariadb',
        'PORT': '3306',
        'OPTIONS': {
            'read_default_file': '../etc/docker/mariadb/config/general-log.cnf',
        }
    }
}

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'swe578_elasticsearch:9200',
    },
}

AUTH_USER_MODEL = 'members.Member'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

LOGIN_REDIRECT_URL = 'members.home'
LOGOUT_REDIRECT_URL = 'login'

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = '/app/' + STATIC_URL

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOCATION_FIELD_PATH = 'location_field'

LOCATION_FIELD = {
    'map.provider': 'google',
    'map.zoom': 8,
    'map.latitude': 41.004292317760786,
    'map.longitude': 28.634627641985492,

    'search.provider': 'google',
    'search.suffix': '',

    # Google
    'provider.google.api': '//maps.google.com/maps/api/js?sensor=false',
    'provider.google.api_key': '',
    'provider.google.api_libraries': '',
    'provider.google.map.type': 'ROADMAP',
    'resources.root_path': '/' + STATIC_URL + LOCATION_FIELD_PATH,
    'resources.media': {
        'js': (
            LOCATION_FIELD_PATH + '/js/form.js',
        ),
    },
}

EASY_MAPS_GOOGLE_KEY = ''
EASY_MAPS_CENTER = (-41.3, 32)
