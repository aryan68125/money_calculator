"""
Django settings for money_calculator project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import django_heroku
from datetime import timedelta
import os

#make error messages into danger so that bootstrap can understand it and style it properly
#before your do that you need to import messages
from django.contrib import messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
#the TEMPLATE_DIRS is necessary so that django knows where your templates are stored for this PROJECT_ROOT
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o8n8*rzdm=$x9sq-$2n$jpg^_6ur&im8@=*d3f%i0mcqon9ilb'

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

    #register your expenses app
    'expenses.apps.ExpensesConfig',

    #register your UserIncome app
    'userincome.apps.UserincomeConfig',

    #django website api section
    #django cleanup will delete any static files images when the model is deleted
    'django_cleanup.apps.CleanupConfig',

    #add boto3 and django-storages here so that we can use amazon s3 bucket
    'storages',

    #add userpreferences app in installed apps this app will keep track of user preferences
    'userpreferences.apps.UserpreferencesConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    #whitenoise for serving our static files in production environment
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'money_calculator.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
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

WSGI_APPLICATION = 'money_calculator.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

#connect your django project to a local production postgresSQL database server
#this postgreSQL can be managed by pgadmin4
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'incomeexpensesdb',
        'USER': 'postgres',
        'PASSWORD': 'Ilovetoneystark',
        'HOST': '127.0.0.1',
        'PORT': 5432,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

#configure MEDIA_URL so that we can connect and display the uploaded image that is present in the static/images folder to our front end from the static folder via models.py file since our images url are gonna be dynamic
MEDIA_URL = '/images/'

#now add the static urls here for this website
#static is like graphics icons and all that stuff for your website including your flex boxes
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

#STATIC_ROOT defines where our static files in production are gonna be when I say production that means we will be setting debugging= False
#collect static is a command that we will use to run STATIC_ROOT
#collect static is a command that will tell django to take all the files in the static folder and its gonna bundle them up in one file and django can take care of that from there
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#configuring the path where the images should be stored when a user uploads his/her images into the website
#by default the images uploaded by the user will be stored in the root directory of the project
#but we want django to store our images uploaded by the users into this path (static/images/)
#MEDIA_ROOT simply tells django where to store user uploaded content
MEDIA_ROOT = os.path.join(BASE_DIR,'static/images')

#email send related settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'userpiyush6@gmail.com'
EMAIL_HOST_PASSWORD = 'wcnvtyexogcbscee'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

django_heroku.settings(locals())

#make error messages into danger so that bootstrap can understand it and style it properly
MESSAGE_TAGS = {
    messages.ERROR : 'danger'
}
