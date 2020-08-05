from .settings import *
import dj_database_url

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES['default'] = dj_database_url.config()

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ALLOWED_HOSTS = ['somae.herokuapp.com']

SECRET_KEY = '$q_k_b=4q!py7d1^t3^b83xtff1_mr=2l_2po1)+x1)9rv$qy5'
