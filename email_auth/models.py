import logging
import string
import uuid

import email_utils
from django.conf import settings
from django.db import models
from django.utils import crypto, timezone
from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger(__name__)


# Warning: changing this value requires database migrations as it
# affects the length of all columns that store tokens.
TOKEN_LENGTH = 64


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


def generate_token():
    """
    Create a random token.

    Returns:
        A random alphanumeric string.
    """
    return crypto.get_random_string(
        allowed_chars=string.ascii_letters + string.digits, length=TOKEN_LENGTH
    )


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
        ordering = ("time_created",)
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

    def send_already_verified(self):
        """
        Send an email notifying the user that this email address has
        already been verified.
        """
        context = {"email": self}
        template = "email_auth/emails/already-verified"

        email_utils.send_email(
            context=context,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.address],
            subject=_("Your Email Address has Already Been Verified"),
            template_name=template,
        )

    def send_duplicate_notification(self):
        """
        Send an email notifying the user that this email address has
        already been registered.
        """
        context = {"email": self}
        template = "email_auth/emails/duplicate-email"

        email_utils.send_email(
            context=context,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.address],
            subject=_("Your Email Address has Already Been Registered"),
            template_name=template,
        )

    def send_verification_email(self):
        """
        Create and send a verification email to the address associated
        with the instance.

        Returns:
            The created :py:class:`EmailVerification` instance.
        """
        verification = EmailVerification.objects.create(email=self)
        verification.send_email()

        return verification

    def verify(self):
        """
        Mark the email address instance as verified.
        """
        self.is_verified = True
        self.time_verified = timezone.now()

        logger.info("Verified email address %s", self.address)

        self.save()


class EmailVerification(models.Model):
    """
    A token that allows a user to verify that they own an email address.

    Ownership is established by emailing the user a random token to the
    email address they provided. If they can provide that token, we
    assume they own the email address it was sent to.
    """

    email = models.ForeignKey(
        "email_auth.EmailAddress",
        help_text=_("The email address that the token is meant to verify."),
        on_delete=models.CASCADE,
        related_name="verifications",
        related_query_name="verification",
        verbose_name=_("email address"),
    )
    time_created = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The time that the instance was created."),
        verbose_name=_("creation time"),
    )
    time_sent = models.DateTimeField(
        blank=True,
        help_text=_("The time that the token was emailed out."),
        null=True,
        verbose_name=_("sent time"),
    )
    time_updated = models.DateTimeField(
        auto_now=True,
        help_text=_("The time of the last update to the instance."),
        verbose_name=_("last update time"),
    )
    token = models.CharField(
        default=generate_token,
        help_text=_("The random token identifying the verification request."),
        max_length=TOKEN_LENGTH,
        primary_key=True,
        verbose_name=_("token"),
    )

    class Meta:
        ordering = ("time_created",)
        verbose_name = _("email verification")
        verbose_name_plural = _("email verifications")

    def __repr__(self):
        """
        Returns:
            A string representation of the instance suitable for
            debugging purposes.
        """
        return build_repr(
            self,
            ["email", "time_created", "time_sent", "time_updated", "token"],
        )

    def __str__(self):
        """
        Returns:
            A description of the email address that this verification
            is for.
        """
        return f"Verification for {self.email}"

    def send_email(self):
        """
        Send an email containing the verification token to the email
        address being verified.
        """
        context = {
            "email": self.email,
            "user": self.email.user,
            "verification": self,
        }
        template = "email_auth/emails/verify-email"

        email_utils.send_email(
            context=context,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email.address],
            subject=_("Please Verify Your Email Address"),
            template_name=template,
        )

        self.time_sent = timezone.now()
        self.save()

    def verify(self):
        """
        Mark the associated email address as verified and delete the
        verification instance.
        """
        self.email.verify()
        self.delete()


class PasswordReset(models.Model):
    """
    A model containing a token that can be used to reset a user's
    password.
    """

    email = models.ForeignKey(
        EmailAddress,
        help_text=_("The email address that the reset token is sent to."),
        on_delete=models.CASCADE,
        related_name="password_resets",
        related_query_name="password_reset",
        verbose_name=_("email"),
    )
    time_created = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The time that the instance was created."),
        verbose_name=_("creation time"),
    )
    time_sent = models.DateTimeField(
        blank=True,
        help_text=_("The time that the token was emailed out."),
        null=True,
        verbose_name=_("sent time"),
    )
    time_updated = models.DateTimeField(
        auto_now=True,
        help_text=_("The time of the last update to the instance."),
        verbose_name=_("last update time"),
    )
    token = models.CharField(
        default=generate_token,
        help_text=_("The random token identifying the password reset."),
        max_length=TOKEN_LENGTH,
        primary_key=True,
        verbose_name=_("token"),
    )

    class Meta:
        ordering = ("time_created",)
        verbose_name = _("password reset")
        verbose_name_plural = _("password resets")

    def __repr__(self):
        """
        Returns:
            A complete string representation of the instance, suitable
            for debugging purposes.
        """
        return build_repr(
            self,
            ["email", "time_created", "time_sent", "time_updated", "token"],
        )

    def __str__(self):
        """
        Returns:
            A string describing the email address the password reset is
            associated with.
        """
        return f"Password reset for '{self.email}'"

    def send_email(self):
        """
        Send the token authorizing the password reset to the email
        address associated with the instance.
        """
        context = {"password_reset": self}

        email_utils.send_email(
            context=context,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email.address],
            subject=_("Reset Your Password"),
            template_name="email_auth/emails/reset-password",
        )

        self.time_sent = timezone.now()
        self.save()
