#-*- coding: utf-8 -*-

"""
Django settings for hcar project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^w^04q--ywbawxll)i!i2m%g*_171-!5*-0#i*)6nht3x+j#i)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = '*'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',    # 세션 사용을 위함
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',    # REST 및 serialization을 사용하기 위함
    'newcar',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',    # 세션 사용을 위함
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hcar.urls'

WSGI_APPLICATION = 'hcar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hcar',
        'USER': 'kshong',
        'PASSWORD': 'kiso2ft',
        'HOST': '*',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ko-KR'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# HTML의 기본 렌더러를 BrowsableAPI에서 HTMl로 변경
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES' : (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
    )
}

# 템플릿 디렉토리 지정
TEMPLATE_DIRS = ( os.path.join(BASE_DIR, 'templates'), )

# 메일서버 설정
#M_EMAIL = 'kshong@coche.dnip.net'
#SERVER_EMAIL = 'kshong@coche.dnip.net'
EMAIL_USE_TLS = True
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'kshong'
EMAIL_HOST_PASSWORD = 'kyh02057'
