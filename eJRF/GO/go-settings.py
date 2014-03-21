import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "%s" % os.environ['DB_NAME'],
        "USER": "%s" % os.environ['DB_USER'],
        "PASSWORD": "%s" % os.environ['DB_PASSWORD'],
        "HOST": "localhost",
    }
}

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_nose',
    'south',
    'lettuce.django',
    'django_extensions',
    'bootstrap_pagination',
    'questionnaire'
)

LETTUCE_AVOID_APPS = (
        'south',
        'django_nose',
        'django_extensions',
        'bootstrap_pagination',
)

SOUTH_TESTS_MIGRATE = False

import logging

south_logger = logging.getLogger('south')
south_logger.setLevel(logging.INFO)

SITE_ID = 1