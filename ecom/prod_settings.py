from .settings import *

import dj_database_url

DEBUG = False
TEMPLATE_DEBUG = False
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

ALLOWED_HOSTS = ['somae.herokuapp.com','https://somae.herokuapp.com','somaele.osc-fr1.scalingo.io','https://somaele.osc-fr1.scalingo.io']

SECRET_KEY = '$q_k_b=4q!py7d1^t3^b83xtff1_mr=2l_2po1)+x1)9rv$qy5'

