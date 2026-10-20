
"""
Django settings for isyswear project.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SECURITY
# ============================================================

# LOCAL DEVELOPMENT FALLBACK ONLY.
# In Render, set SECRET_KEY to a new, strong, private value.
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'dev-only-insecure-key-change-this-for-local-use'
)

# Render will set DEBUG=False.
DEBUG = os.environ.get('DEBUG', 'True').strip().lower() == 'true'

# Set ALLOWED_HOSTS in Render to your actual Render hostname.
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        'ALLOWED_HOSTS', '127.0.0.1,localhost'
    ).split(',')
    if host.strip()
]

# Set this in Render to your actual HTTPS website URL.
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
    if origin.strip()
]

# Needed when Django is behind Render's HTTPS proxy.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'adminpanel',
    'products',
    'orders',
    'cart',
    'users',
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Serves collected static files in production.
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ============================================================
# URLS AND TEMPLATES
# ============================================================

ROOT_URLCONF = 'isyswear.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'isyswear.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'isyswear.wsgi.application'


# ============================================================
# DATABASE
# ============================================================

# If DB_HOST exists, use the Aiven database configured through
# environment variables (Render production).
#
# Otherwise, use your local WAMP/MySQL database.

if os.environ.get('DB_HOST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'defaultdb'),
            'USER': os.environ.get('DB_USER', 'avnadmin'),

            # Set DB_PASSWORD in Render. Do not put it in GitHub.
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),

            'HOST': os.environ['DB_HOST'],
            'PORT': os.environ.get('DB_PORT', '24199'),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'ssl': {
                    # Keep aiven-ca.pem beside manage.py.
                    'ca': str(BASE_DIR / 'aiven-ca.pem'),
                },
            },
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'dbIsyswear',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True


# ============================================================
# STATIC AND MEDIA FILES
# ============================================================

STATIC_URL = '/static/'

# Source directory containing your CSS, JavaScript, and images.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Destination for python manage.py collectstatic.
STATIC_ROOT = os.path.join(BASE_DIR, '.static_prod')

# WhiteNoise serves collected static files in production.
STATICFILES_STORAGE = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)

# Uploaded product images and other user uploads.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ============================================================
# AUTHENTICATION AND REDIRECTS
# ============================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'


# ============================================================
# EMAIL
# ============================================================

# Keeps the existing console email backend.
# Emails are printed to the server console, not actually sent.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@isyswear.local'

PASSWORD_RESET_TIMEOUT = 3600  # 1 hour
