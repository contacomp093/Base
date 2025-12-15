"""
Django settings for core project.
"""
import dj_database_url
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv


# --------------------------------------------
# CARGAR VARIABLES DESDE .env
# --------------------------------------------

# Carga archivo .env ubicado en la raíz del proyecto
load_dotenv()

# --------------------------------------------
# BASE
# --------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY Y DEBUG vienen desde el .env
SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-no-usar-en-produccion")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    "base-40xl.onrender.com",
    "localhost",
    "127.0.0.1",
]


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
    'accounts.apps.AccountsConfig',
    'dashboard',
    
]


# --------------------------------------------
# MIDDLEWARE
# --------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',

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
    'default': dj_database_url.config(
        default=os.getenv("DATABASE_URL")
    )
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
# INTERNACIONALIZACIÓN
# --------------------------------------------

LANGUAGE_CODE = 'es'

USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('es', _('Español')),
    ('en', _('English')),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

LANGUAGE_COOKIE_NAME = 'django_language'


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
LOGOUT_REDIRECT_URL = "/accounts/login/"


# ============================================
# SENDGRID - Email API (Recommended for Render)
# ============================================

# Backend que usa la API HTTP de SendGrid (NO SMTP)
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"

# Tu API Key (se lee desde variables de entorno)
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

# Debe estar desactivado para que envíe correos reales
SENDGRID_SANDBOX_MODE_IN_DEBUG = False

# Remitente verificado en SendGrid (Single Sender)
DEFAULT_FROM_EMAIL = "contacomp093@gmail.com"

# Dominio para enlaces en correos
DEFAULT_DOMAIN = "https://base-40xl.onrender.com"

# ============================================
# DOMINIO BASE PARA EMAILS
# ============================================

DEFAULT_DOMAIN = os.getenv(
    "DEFAULT_DOMAIN",
    "http://127.0.0.1:8000" if DEBUG else "https://base-40xl.onrender.com"
)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


