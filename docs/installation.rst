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

*************
Configuration
*************

Add ``email_auth`` to your ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        # Django apps

        # Third party apps
        "email_auth",
        # More third party apps

        # Your custom apps
    ]

Next ensure Django is `set up to send emails <django-emails>`_. Additionally,
ensure ``DEFAULT_FROM_EMAIL`` is set. This is the address that all account
related emails such as email verifications and password reset emails are sent
from.

.. _django-emails: https://docs.djangoproject.com/en/dev/topics/email/
.. _django-simple-email-auth-pypi: https://pypi.org/project/django-simple-email-auth/
