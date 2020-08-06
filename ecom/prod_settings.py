from .settings import *

import dj_database_url
import django_heroku

DEBUG = False
TEMPLATE_DEBUG = False
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

ALLOWED_HOSTS = ['somae.herokuapp.com']

SECRET_KEY = '$q_k_b=4q!py7d1^t3^b83xtff1_mr=2l_2po1)+x1)9rv$qy5'

django_heroku.settings(locals())

MEDIA_URL = '/media.somae.herokuapp.com/'