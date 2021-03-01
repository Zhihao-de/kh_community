"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4ut0sq)46^$6ou)ypkmx2n*kqfux9b-%2d&%6rjx=01&=l1q!a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'corsheaders',
    'rest_framework',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.tests',
    'modelcluster',
    'taggit',

    'attachments.apps.AttachmentsConfig',
    'products.apps.ProductsConfig',
    'orders.apps.OrdersConfig',
    'intentions.apps.IntentionsConfig',
    'users.apps.UsersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'server.urls'

FRONTEND_BASE_DIR = 'cms/dist'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [FRONTEND_BASE_DIR],
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

WSGI_APPLICATION = 'server.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

AUTH_PROFILE_MODULE = 'djangoadmin.myadmin.UserProfile'

DATABASES = {

    #        'default': {
    #            'ENGINE': 'django.db.backends.mysql',
    #            'NAME': 'khdb',
    #            'HOST': '106.54.170.236',
    #            'PORT': '3306',
    #            'USER': 'khdb',
    #            'PASSWORD': 'BYmr82236130@'
    #        }

    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'khdb',
        'HOST': '81.71.33.22',
        'PORT': '3306',
        'USER': 'khdb',
        'PASSWORD': 'BYmr82236130@'
    }

}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, FRONTEND_BASE_DIR),
    os.path.join(BASE_DIR, FRONTEND_BASE_DIR, 'static'),
]

# Django Rest Framework settings

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),  # 全局默认配置过滤

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',  # JWT认证，在前面的认证方案优先
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# DRF扩展
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_USER_CACHE': 'default'

}

# CACHES = {
#    "default": {
#        "BACKEND": "django_redis.cache.RedisCache",
#        "LOCATION": "redis://106.54.170.236:6379",
#        "OPTIONS": {
#            "CLIENT_CLASS": "django_redis.client.DefaultClient",
#            #   "password": "BYmr82236130"
#        }
#    }
# }

# 配置session缓存
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

import datetime

JWT_AUTH = {
    'JWT_AUTH_HEADER_PREFIX': 'kh',  # "Authorization: JWT <token>"
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=90),  # JWT_EXPIRATION_DELTA 指明token的有效期
}

# 配置MQ
RABBITMQCONFIG = {
    'username': 'admin',
    'password': 'admin'

}

# Wagtail settings
# http://docs.wagtail.io/en/v2.8/getting_started/integrating_into_django.html

WAGTAIL_SITE_NAME = '开皇社区页面管理'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/files/'

UPLOAD_ROOT = os.path.join(MEDIA_ROOT, 'files')
UPLOAD_URL = '/media/files/'
MCH_ID = '1533682051'
MCH_KEY = 'szsddj2016010691440300359586730K'
NOTIFY_URL = 'http://api.kaihuangliulian.com/v1/orders/wxpayback/'
NOTIFY_URL_REFUND = 'http://api.kaihuangliulian.com/v1/internal/orders/refundback/'
CERT_PATH = ''
KEY_PATH = ''

# 小程序appid

WEIXIN_APPID = 'wxa20b6f7055206dd4'
# 小程序SECRET
WEIXIN_SECRET = 'd891da84557b9f77e03d8b66f53d88ed'

"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}
"""
