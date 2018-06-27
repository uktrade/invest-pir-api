import os

from config.settings import *  # noqa
from config.settings import PROJECT_ROOT

CELERY_ALWAYS_EAGER = True
BROKER_BACKEND = 'memory'
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

REST_FRAMEWORK = {}
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = "/media/"
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
