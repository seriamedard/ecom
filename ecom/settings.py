import os
from re import DEBUG
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 'tbwiiy^g@tb-!z+qu0qhhlqn6_%u+sife#5pl=o385=5=cej&(')


DEBUG = os.environ.get("DEBUG", True)

# ADMINS = (
#         ('asus', 'seria.medard.pge2018@gmail.com'),
#     )

# MANAGERS = ADMINS

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'admin_interface',
    'colorfield',
    'boutique',
    'debug_toolbar',
    'ckeditor',
    'ckeditor_uploader',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
]

ROOT_URLCONF = 'ecom.urls'

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
                'ecom.context_processors.get_variable',
                'ecom.context_processors.get_variable_panier',
                'django.template.context_processors.media',
            ],
        },
    },
]
 
WSGI_APPLICATION = 'ecom.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if os.environ.get("DJANGO_ENV") == 'production':
    print('je suis en production')
    DEBUG = False
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'))
    }
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    ALLOWED_HOSTS = ['somma-electronic-0023d7028e18.herokuapp.com',
                     '*.somma-electronic-0023d7028e18.herokuapp.com',
                     'www.somma-electronic-0023d7028e18.herokuapp.com',]

    CSRF_TRUSTED_ORIGINS = [
        'https://www.somma-electronic-0023d7028e18.herokuapp.com',
        'https://somma-electronic-0023d7028e18.herokuapp.com',
    ]
else:
    print('je suis en developpement')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


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

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'seriamedard@gmail.com'
EMAIL_HOST_PASSWORD = 'wksijjjuypnrlaan'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

INTERNAL_IPS = [
    '127.0.0.1',
]

DEFAULT_CHARSET = 'utf-8'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/



STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Path media such as image
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# StaticFiles
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
"""
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)
"""

STATIC_URL = '/staticfiles/'

# Ckeditor
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'extraPlugins': ','.join([
            'mathjax',
            'html5video',
            'widget',
            'widgetselection',
            'clipboard',
            'lineutils',
            'emoji',
            'autocomplete',
            'textwatcher',
            'textmatch',
            'panelbutton',
            'floatpanel',
            'panel',
            'button',
            'xml',
            'ajax',
            'embed'
        ]),
    }
}

CKEDITOR_UPLOAD_PATH = "media/"

X_FRAME_OPTIONS = 'SAMEORIGIN'

LOGIN_URL = '/boutique/connexion/'
