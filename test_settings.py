import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "email_auth",
    "email_auth.interfaces.rest",
]

SECRET_KEY = "secret"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
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
