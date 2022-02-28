"""
Django settings for saasboilerplate project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import json
import os
from pathlib import Path
from urllib import request

import environ
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate
from django.contrib.auth import get_user_model

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY", default="this-should-not-be-your-secret")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Setup allowed hosts with the defined environmental variable if existing
# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = (
    env("WEBSITE_HOSTNAME").split(" ") if "WEBSITE_HOSTNAME" in env.ENVIRON else []
)


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "django_drf_filepond",
    "usermanagement",
    "corsheaders",
    "django_extensions",
    "djmoney",
    "drf_app_generators",
    "rest_framework_jwt",
    "djstripe",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "saasboilerplate.urls"

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

WSGI_APPLICATION = "saasboilerplate.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": env("DBENGINE", cast=str, default="django.db.backends.sqlite3"),
        "NAME": env("DBNAME", cast=str, default=BASE_DIR / "db.sqlite3"),
        "HOST": env("DBHOSTNAME", cast=str, default="localhost"),
        "USER": env("DBUSER", cast=str, default="user"),
        "PASSWORD": env("DBPASS", cast=str, default="password"),
        "PORT": env("DBPORT", cast=str, default="5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# REST Framework

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
}


# Cross Origin Handling
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = (
    "content-disposition",
    "accept-encoding",
    "content-type",
    "accept",
    "origin",
    "authorization",
)


# Filepond configuration
DJANGO_DRF_FILEPOND_UPLOAD_TMP = os.path.join(BASE_DIR, "filepond-temp-uploads")
DJANGO_DRF_FILEPOND_FILE_STORE_PATH = os.path.join(BASE_DIR, "filepond-stored-uploads")


# Custom User Model
AUTH_USER_MODEL = "usermanagement.MyUser"


# Default auto field
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

AUTH0_DOMAIN = env(
    "VUE_APP_AUTH0_DOMAIN",
    default="",
)
API_IDENTIFIER = env(
    "VUE_APP_AUTH0_API_IDENTIFIER",
    default="",
)
PUBLIC_KEY = None
JWT_ISSUER = None

if AUTH0_DOMAIN:
    jsonurl = request.urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read().decode("utf-8"))
    cert = (
        "-----BEGIN CERTIFICATE-----\n"
        + jwks["keys"][0]["x5c"][0]
        + "\n-----END CERTIFICATE-----"
    )
    certificate = load_pem_x509_certificate(cert.encode("utf-8"), default_backend())
    PUBLIC_KEY = certificate.public_key()
    JWT_ISSUER = "https://" + AUTH0_DOMAIN + "/"


def jwt_get_username_from_payload_handler(payload):
    """This method is used to map the username from the access_token payload to the Django user"""

    try:
        user = get_user_model().objects.get(auth_provider_sub=payload["sub"])
        print("User exists")
        return user.auth_provider_sub
    except get_user_model().DoesNotExist:
        print("User does not exist")
        print(payload)
        user = get_user_model().objects.create_user(
            auth_provider_sub=payload["sub"], is_active=True
        )
        print(user)
        return jwt_get_username_from_payload_handler(payload)


JWT_AUTH = {
    "JWT_PAYLOAD_GET_USERNAME_HANDLER": jwt_get_username_from_payload_handler,
    "JWT_PUBLIC_KEY": PUBLIC_KEY,
    "JWT_ALGORITHM": "RS256",
    "JWT_AUDIENCE": API_IDENTIFIER,
    "JWT_ISSUER": JWT_ISSUER,
    "JWT_AUTH_HEADER_PREFIX": "Bearer",
}

# Emails are send to the console, if an email server is not defined through environmental variables
if (
    "EMAIL_BACKEND" in env.ENVIRON
    and "EMAIL_HOST" in env.ENVIRON
    and "EMAIL_PORT" in env.ENVIRON
    and "EMAIL_USE_TLS" in env.ENVIRON
    and "EMAIL_HOST_USER" in env.ENVIRON
    and "EMAIL_HOST_PASSWORD" in env.ENVIRON
):
    EMAIL_BACKEND = env("EMAIL_BACKEND")
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_PORT = env("EMAIL_PORT")
    EMAIL_USE_TLS = env("EMAIL_USE_TLS", bool)
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
    SERVER_EMAIL = env("EMAIL_FROM")
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


### Settings for customization
# Enter the name of your site. It will be used, e.g., in emails
SITE_NAME = "SimplySaaS"


### Stripe configuration
STRIPE_LIVE_SECRET_KEY = env(
    "STRIPE_LIVE_SECRET_KEY",
    default="",
)
STRIPE_TEST_SECRET_KEY = env(
    "STRIPE_TEST_SECRET_KEY",
    default="",
)
STRIPE_LIVE_MODE = False
# Get your webhook secret from the section in the Stripe dashboard
# where you added the webhook endpoint
DJSTRIPE_WEBHOOK_SECRET = env(
    "DJSTRIPE_WEBHOOK_SECRET",
    default="",
)
DJSTRIPE_USE_NATIVE_JSONFIELD = True
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"
