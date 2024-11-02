"""
Django settings for myhandmade project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import cloudinary_storage
import os

from dotenv import load_dotenv # type: ignore

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^7^i!67h37-dvqr9y_eu1sofsvuu$9u*9)9g#2hktu)z_4f-u1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backend.apps.users',
    'backend.apps.chat',
    'backend.apps.channels',
    'backend.apps.reviews',
    'backend.apps.products',
    'backend.apps.orders',
    'backend.apps.notifications',
    'backend.apps.dashboard',
    'backend.apps.analytics',
    'backend.apps.admin_panel',
    'backend.apps.stores',
    'backend.apps.categories',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_celery_beat',
    'rest_framework.authtoken',
    'cloudinary_storage',
    'cloudinary',
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

ROOT_URLCONF = 'backend.urls'

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

# WSGI_APPLICATION = 'backend.wsgi.application'

ASGI_APPLICATION = 'backend.wsgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}




# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',        # Supabase database name
        'USER': 'postgres.cwclpnpkglzoscohzvnx',        # Supabase user
        'PASSWORD': 'Myhandmade#pass', # Supabase password
        'HOST': 'aws-0-ap-southeast-1.pooler.supabase.com',         # Supabase host, e.g., db.supabase.co
        'PORT': '6543',                       # Default PostgreSQL port
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'users.User'  # Assuming your app is named 'users'

# REST_FRAMEWORK = {
#     # 'DEFAULT_AUTHENTICATION_CLASSES': ( ),
#     "TOKEN_JWT_AUTHENTICATION":  "rest_framework_simplejwt.authentication.JWTAuthentication",
#     "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
#     "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
#     "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
#     "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
#     "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
# }


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        # You can add more authentication classes if needed, e.g. for JWT
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Email credentials
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'koodi.cloud@gmail.com'
EMAIL_HOST_PASSWORD = 'gvje nsms jjdw lfnb'

# EMAIL_HOST = 'smtp.resend.com'
# EMAIL_PORT = 465
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'resend' 
# EMAIL_HOST_PASSWORD = 'Myhandmade#pass' #'re_epeYK9t8_MyLFnaiAJZdSJbSBJfxVDW6v'

# SUPABASE_URL = 'https://cwclpnpkglzoscohzvnx.supabase.co'
# SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3Y2xwbnBrZ2x6b3Njb2h6dm54Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAzNjc3NjcsImV4cCI6MjA0NTk0Mzc2N30.6SY6KC0cGnTs1QRNqDhuPCyHzcodSkjpp1swTclo8xk'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUD_NAME'),
    'API_KEY': os.environ.get('API_KEY'),
    'API_SECRET': os.environ.get('API_SECRET'),
}

# make cloudinary default file storage 

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# import cloudinary
# import cloudinary.uploader
# import cloudinary.api

# # Cloudinary Configuration
# cloudinary.config(
#     cloud_name= os.environ.get('your_cloud_name'),  # replace with your cloud name
#     api_key= os.environ.get('your_api_key'),         # replace with your API key
#     api_secret= os.environ.get('your_api_secret')    # replace with your API secret
# )




# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

