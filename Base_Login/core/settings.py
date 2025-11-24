"""
Django settings for core project.
"""

import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# --------------------------------------------
# BASE
# --------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-7a*h6*4x3j5u@s=2^bhvi3-a!g6@ecnu+tu-86ds549i&&4ln4'
DEBUG = True
ALLOWED_HOSTS = ['*']


# --------------------------------------------
# APLICACIONES
# --------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'dashboard',
]


# --------------------------------------------
# MIDDLEWARE
# --------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # ← IMPORTANTE PARA TRADUCCIONES

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# --------------------------------------------
# URLS & WSGI
# --------------------------------------------

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'


# --------------------------------------------
# TEMPLATES
# --------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# --------------------------------------------
# BASE DE DATOS
# --------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# --------------------------------------------
# VALIDADORES DE CONTRASEÑA
# --------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --------------------------------------------
# INTERNACIONALIZACIÓN (CORREGIDO)
# --------------------------------------------

LANGUAGE_CODE = 'es'   # idioma por defecto

USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('es', _('Español')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

LANGUAGE_COOKIE_NAME = 'django_language'  # ← SIN ESTO NO CAMBIA


# --------------------------------------------
# ARCHIVOS ESTÁTICOS
# --------------------------------------------

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"


# --------------------------------------------
# LOGIN / LOGOUT
# --------------------------------------------

LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = '/accounts/login/'



EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "contacomp093@gmail.com"
EMAIL_HOST_PASSWORD = "wcax huzv tuqc dkaz"
DEFAULT_FROM_EMAIL = "Sistema de citas <contacomp093@gmail.com>"

# Dominio base para enlaces en correos (PRODUCCIÓN)
DEFAULT_DOMAIN = "https://base-40xl.onrender.com"