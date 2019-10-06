.. _app-settings:

########
Settings
########

Settings are provided as a dictionary named ``EMAIL_AUTH`` in the Django
settings file. For example::

    # settings.py

    EMAIL_AUTH = {
        "EMAIL_VERIFICATION_URL": "https://example.com/{key}"
    }

.. _email-verification-url:

**************************
``EMAIL_VERIFICATION_URL``
**************************

Default
  ``None``

Example
  ``https://my-frontend.com/verify-email/{key}``

A template used to construct the URL of the page that users visit to verify
their email. The placeholder ``{key}`` will be replaced with the verification
token.

.. _password-reset-url:

**********************
``PASSWORD_RESET_URL``
**********************

Default
  ``None``

Example
  ``https://my-frontend.com/reset-password/{key}``

A template used to construct the URL of the page that users visit to reset their
password. The placeholder ``{key}`` will be replaced with the reset token.
