"""
Settings specific to ``simple_email_auth``.

The setting implementation is modeled on "Django Allauth's" from:
https://github.com/pennersr/django-allauth/blob/master/allauth/account/app_settings.py
"""

import sys
from typing import Optional


class AppSettings(object):
    def _setting(self, name: str, default: any):
        """
        Retrieve a setting from the current Django settings.

        Settings are retrieved from the ``EMAIL_AUTH`` dict in the
        settings file.

        Args:
            name:
                The name of the setting to retrieve.
            default:
                The setting's default value.

        Returns:
            The value provided in the settings dictionary if it exists.
            The default value is returned otherwise.
        """
        from django.conf import settings

        settings_dict = getattr(settings, "EMAIL_AUTH", {})

        return settings_dict.get(name, default)

    @property
    def EMAIL_VERIFICATION_URL(self) -> Optional[str]:
        """
        The template to use for the email verification url.
        """
        return self._setting("EMAIL_VERIFICATION_URL", None)

    @property
    def PASSWORD_RESET_URL(self) -> Optional[str]:
        """
        The template to use for the password reset url.
        """
        return self._setting("PASSWORD_RESET_URL", None)


# Ugly? Guido recommends this himself ...
# http://mail.python.org/pipermail/python-ideas/2012-May/014969.html

app_settings = AppSettings()
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings
