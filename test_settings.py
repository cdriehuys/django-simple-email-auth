import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = "secret"


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "email_auth.interfaces.rest",
    "email_auth",
]


MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        # Normally we would use an in-memory database for testing by setting
        # "NAME" to ":memory:", but we get errors using the "live_server"
        # fixture if we do that. It's unclear if this means tests are using a
        # real file for database access or if they are still using an in-memory
        # database.
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


ROOT_URLCONF = "test_urls"


# Need a static URL in order for our server to actually be reached for some
# reason.
STATIC_URL = "/static/"
