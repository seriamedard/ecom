from .settings import *

import dj_database_url

DEBUG = True
TEMPLATE_DEBUG = True
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

ALLOWED_HOSTS = ['somae.herokuapp.com','https://somae.herokuapp.com','media/images']

SECRET_KEY = '$q_k_b=4q!py7d1^t3^b83xtff1_mr=2l_2po1)+x1)9rv$qy5'

DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'

DROPBOX_OAUTH2_TOKEN = 'o4WwD5rIzSAAAAAAAAAAAfOKKdf82hfN03X9YA3WE0BVJYvlZa0zVgVsbs-1hpoR'
