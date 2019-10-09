############
Installation
############

************
Requirements
************

The following requirements are supported. Other setups may work, but they are
not officially supported.

* Python >= 3.6
* Django >= 2.1

************
Installation
************

From `PyPI <django-simple-email-auth-pypi>`_ (Recommended)::

    pip install django-simple-email-auth

From GitHub (latest code)::

    pip install git+https://github.com/cdriehuys/django-simple-email-auth.git

Extra Dependencies
==================

If you would like to use the provided REST endpoints, make sure you install
``djangorestframework`` either manually or using the ``[rest]`` extras::

    # Manually
    pip install djangorestframework

    # Using the "rest" extras
    pip install django-simple-email-auth[rest]

*************
Configuration
*************

Add ``email_auth`` to your ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        # Django apps

        # Third party apps

        # If you would like to use the provided REST API:
        "email_auth.interfaces.rest",
        "rest_framework",

        # Core models and templates:
        "email_auth",

        # More third party apps

        # Your custom apps
    ]

Note the order that you include the apps in is important. In particular,
``email_auth.interfaces.rest`` overrides some templates provided by the core
``email_auth``. In order for this to work, the overriding app has to be listed
first so that Django finds its templates first.

Next ensure Django is `set up to send emails <django-emails_>`_. Additionally,
ensure ``DEFAULT_FROM_EMAIL`` is set. This is the address that all account
related emails such as email verifications and password reset emails are sent
from.

URLs
====

If you are using the included REST endpoints, be sure to include the URLs in
your :file:`urls.py`::

    urlpatterns = [
        # Other URLs...
        path("/accounts/", include("email_auth.interfaces.rest.urls")),
        # More URLs...
    ]

App Configuration
=================

See :ref:`app-settings` for application-specific configuration options.

.. _django-emails: https://docs.djangoproject.com/en/dev/topics/email/
.. _django-simple-email-auth-pypi: https://pypi.org/project/django-simple-email-auth/
