DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "ejrf_test",
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "localhost",
    }
}

LETTUCE_AVOID_APPS = (
        'south',
        'django_nose',
        'lettuce.django',
        'django_extensions',
        'bootstrap_pagination',
)
