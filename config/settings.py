"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPATE_DIR = os.path.join(BASE_DIR, 'templates')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = 'django-insecure-$%e5_12d&f)u9x&k18p6m!l*mrl#sb51)3$ms+n#usd9c7$wh('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# ALLOWED_HOSTS = ["didattica.jprq.app", '127.0.0.1', "demo.jprq.app"]
ALLOWED_HOSTS = ['98.70.77.175', 'didattica.uz', '.vercel.app', '127.0.0.1', 'localhost', '.jprq.app']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_TRUSTED_ORIGINS = [
    'https://didattica.uz',
    'https://www.didattica.uz',
    'https://98.70.77.175',
    'http://didattica.uz',
    'http://www.didattica.uz',
    'http://98.70.77.175',
    'https://localhost',
    'htpp://127.0.0.1',
    'https://demo.jprq.app',
]

CSRF_COOKIE_SECURE = True


# Application definition

INSTALLED_APPS = [
    'widget_tweaks',
    "debug_toolbar",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'students',
    'teachers',
    'exams',
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# CSRF_COOKIE_SECURE = False
ROOT_URLCONF = 'config.urls'
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPATE_DIR],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres.fclnvhgqfitacxpxcmyg',
#         'PASSWORD': 'YTP%GV8LuZXY2w$',
#         'HOST': 'aws-0-eu-central-1.pooler.supabase.com',
#         'PORT': '5432',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database', # This is where you put the name of the db file.
                 # If one doesn't exist, it will be created at migration time.
    }
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Additional locations of static files
STATICFILES_DIRS = [
    STATIC_DIR,
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# INTERNAL_IPS = [
#     "127.0.0.1",
# ]
