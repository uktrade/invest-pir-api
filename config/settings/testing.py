from config.settings import *  # noqa

CELERY_ALWAYS_EAGER = True
BROKER_BACKEND = 'memory'
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

REST_FRAMEWORK = {}
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
