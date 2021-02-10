from .settings import *

import dj_database_url

DEBUG = False
TEMPLATE_DEBUG = False
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

ALLOWED_HOSTS = ['soma-electronic.herokuapp.com']

SECRET_KEY = "9L}}cE:~pa{\x0bM\tT\x0ci:L\\I\\+Q\x0cAE\t?Cmx>8HGe^tR+i-|z*\x0b^g?"

