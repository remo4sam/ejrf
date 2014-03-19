DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "ejrf.sqlite",
    }
}

LETTUCE_AVOID_APPS = (
        'south',
        'django_nose',
        'lettuce.django',
        'django_extensions',
        'bootstrap_pagination',
)