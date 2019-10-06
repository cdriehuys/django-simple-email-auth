from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EmailAuthRESTInterfaceConfig(AppConfig):
    """
    Default configuration for ``email_auth.interfaces.rest``.
    """

    name = "email_auth.interfaces.rest"
    verbose_name = _("Simple Email Authentication REST Interface")
