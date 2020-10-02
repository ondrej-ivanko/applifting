"""
Django settings for applifting project.

Generated by 'django-admin startproject' using Django 3.1.
"""
import os
import sys
import logging
import dj_database_url

from pathlib import Path
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

localhost = bool(os.getenv("HOST") == "127.0.0.1")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
if localhost:
    load_dotenv(verbose=True, dotenv_path=os.path.join(BASE_DIR, ".env_local_dev"))

SECRET_KEY = os.getenv("SECRET_KEY")

BASE_URL = os.getenv("BASE_URL")
assert BASE_URL, logger.error("BASE_URL environment variable is not set.")


DEBUG = os.getenv("DEBUG", "False")

ALLOWED_HOSTS = ["*"]

APPEND_SLASH = False

# Application definition

INSTALLED_APPS = [
    "catalog",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "crispy_forms",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "applifting.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "applifting.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {}

POSTGRES = {
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    "NAME": os.getenv("NAME"),
    "USER": os.getenv("USER"),
    "PASSWORD": os.getenv("PASSWORD"),
    "HOST": os.getenv("HOST", "127.0.0.1"),
    "PORT": os.getenv("PORT", "5432"),
}

SQLITE = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
}

# reading variables of 'heroku postgres addon' to populate DB settings dictionary
PRODUCTION_DB = dj_database_url.config(ssl_require=True)

WIN = sys.platform.startswith("win")
DATABASES["default"] = PRODUCTION_DB if not localhost else POSTGRES if WIN else SQLITE

# using default locmemcache for local developement and redis cache in production
if not localhost:
    CACHES = {
        "default": {
            "BACKEND": "redis_cache.RedisCache",
            "LOCATION": os.environ.get("REDIS_URL"),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "catalog.exceptions.custom_exception_handler",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

# CELERY STUFF
BROKER_URL = os.getenv("REDIS_URL")
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERYD_TIME_LIMIT = 58
CELERYD_SOFT_TIME_LIMIT = 50
