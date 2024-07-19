"""
Django settings for prestigetuninguz project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path
from django.conf import settings


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_bm*%ivm*y73kfr7(7js3uk0hexl2=2d9#jcn4u6h4xbd2m5g_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
    'DISABLE_PANELS': (
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    ),
    'JQUERY_URL': '', 
}


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'main',
    'api'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'prestigetuninguz.urls'

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

WSGI_APPLICATION = 'prestigetuninguz.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer','rest_framework.renderers.BrowsableAPIRenderer',),
    'DEFAULT_PARSER_CLASSES': ('rest_framework.parsers.JSONParser',),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    },
  
   
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  
    "http://127.0.0.1:8000",   
    "http://localhost:5000",
    "http://*"   

]


CSP_HEADER = {
    'default-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'", "*"],
    'script-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'", "*"],
    'style-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'", "*"],
    'img-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'", "*"],
    'font-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'", "*"],
    'frame-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'", "*"],
    'object-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'", "*"],
}

X_FRAME_OPTIONS = 'ALLOWALL'




CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

SESSION_COOKIE_NAME = "session_cookie"
SESSION_COOKIE_AGE = 1209600
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/file.log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SPECTACULAR_SETTINGS = {
    'TITLE': 'Pyblog API Documentation',
    'DESCRIPTION': 'This API provides endpoints for interacting with our service.',
    'VERSION': '1.0.0',
    'SCHEMA_PATH_PREFIX': r'/api/v1',
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVE_PUBLIC': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'COMPONENT_SPLIT_RESPONSE': True,
    'COMPONENT_SPLIT_PAGINATION': True,
    'COMPONENT_SPLIT_PARAMETERS': True,
    'COMPONENT_SPLIT_SECURITY': True,
    'VALIDATE_REQUEST_BODY': True,
    'VALIDATE_RESPONSE_BODY': True,
    'DEFAULT_GENERATOR_CLASS': 'drf_spectacular.generators.SchemaGenerator',
    'DEFAULT_AUTO_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FIELD_INSPECTORS': [
        'drf_spectacular.inspectors.CamelCaseJSONFilter',
        'drf_spectacular.inspectors.ExcludeSerializerDefault',
        'drf_spectacular.inspectors.SortedParameterInspector',
        'drf_spectacular.inspectors.RecursiveFieldInspector',
    ],
    'DEFAULT_FILTER_INSPECTORS': [
        'drf_spectacular.inspectors.DjangoFilterInspector',
        'drf_spectacular.inspectors.CoreAPICompatInspector',
    ],
    'DEFAULT_PATH_PARAM_INSPECTORS': [
        'drf_spectacular.inspectors.CamelCaseJSONFilter',
    ],
    'DEFAULT_REQUEST_TRANSFORMERS': [
        'drf_spectacular.plumbing.OptionalPaginationTransformer',
    ],
    'DEFAULT_RESPONSE_TRANSFORMERS': [
        'drf_spectacular.plumbing.OptionalPaginationTransformer',
    ],

}



# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
