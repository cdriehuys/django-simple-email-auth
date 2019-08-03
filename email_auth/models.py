import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


def build_repr(instance, fields):
    """
    Build the string representation for an instance.

    Args:
        instance:
            The instance to build the repr for.
        fields:
            A list of fields to include in the repr.

    Returns:
        A string describing the provided instance including
        representations of all specified fields.
    """
    values = [f"{f}={repr(getattr(instance, f))}" for f in fields]

    return f'{instance.__class__.__name__}({", ".join(values)})'


class EmailAddress(models.Model):
    """
    An email address belonging to a user.
    """

    address = models.EmailField(
        db_index=True,
        help_text=_("The user's preferred spelling of their email address."),
        verbose_name=_("address"),
    )
    id = models.UUIDField(
        default=uuid.uuid4,
        help_text=_("A unique identifier for the instance."),
        primary_key=True,
        verbose_name=_("ID"),
    )
    is_verified = models.BooleanField(
        default=False,
        help_text=_(
            "A boolean indicating if the user has confirmed ownership of the "
            "address."
        ),
    )
    normalized_address = models.EmailField(
        help_text=_(
            "The normalized version of the user's email address used for "
            "comparison with other addresses."
        ),
        unique=True,
        verbose_name=_("normalized address"),
    )
    time_created = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The time that the instance was created."),
        verbose_name=_("creation time"),
    )
    time_updated = models.DateTimeField(
        auto_now=True,
        help_text=_("The time of the last update to the instance."),
        verbose_name=_("last update time"),
    )
    time_verified = models.DateTimeField(
        blank=True,
        help_text=_(
            "The time that the user verified ownership of this email address."
        ),
        null=True,
        verbose_name=_("verification time"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        help_text=_("The user who owns the email address."),
        on_delete=models.CASCADE,
        related_name="email_addresses",
        related_query_name="email_address",
        verbose_name=_("user"),
    )

    class Meta:
        ordering = ("normalized_address",)
        verbose_name = _("email address")
        verbose_name_plural = _("email addresses")

    def __repr__(self):
        """
        Returns:
            A complete string representation of the object suitable for
            debugging purposes.
        """
        return build_repr(
            self,
            [
                "address",
                "id",
                "is_verified",
                "normalized_address",
                "time_created",
                "time_updated",
                "time_verified",
                "user",
            ],
        )

    def __str__(self):
        """
        Returns:
            The email's address in the user's preferred format.
        """
        return self.address

    def clean(self):
        """
        Populate derived fields.
        """
        self.normalized_address = self.address.lower()
