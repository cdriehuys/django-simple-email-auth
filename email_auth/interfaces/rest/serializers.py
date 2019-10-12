import logging
from typing import Optional

import email_utils
from django.conf import settings
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from email_auth import models


logger = logging.getLogger(__name__)


class EmailVerificationRequestSerializer(serializers.Serializer):
    """
    Serializer to request re-sending of a verification email.
    """

    email = serializers.EmailField()

    def save(self, **kwargs) -> Optional[models.EmailVerification]:
        """
        Send the appropriate email notification to the provided email
        address. If the email address exists in the database but has not
        been verified, a new verification token is sent. If the email is
        already verified, a notification informing the user their email
        is already verified is sent. If the email does not exist in the
        system, we advice the user to register or add the email address
        to their account first.

        Returns:
            The :py:class:`EmailVerification` instance that was created
            if one was created or else ``None``.
        """
        try:
            email_inst = models.EmailAddress.objects.get(
                address__iexact=self.validated_data["email"]
            )
        except models.EmailAddress.DoesNotExist:
            self._send_missing_email_notification()

            return None

        if email_inst.is_verified:
            email_inst.send_already_verified()

            return None

        verification = models.EmailVerification(email=email_inst)
        verification.send_email()

        return verification

    def _send_missing_email_notification(self):
        """
        Send an email to the provided address informing the user they
        need to register or add the email to their account before they
        can verify it.
        """
        email_utils.send_email(
            context={"email": self.validated_data["email"]},
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.validated_data["email"]],
            subject=_("Unregistered Email Address"),
            template_name="email_auth/emails/unregistered-email",
        )


class EmailVerificationSerializer(serializers.Serializer):
    """
    Serializer used to verify email addresses using verification tokens.
    """

    token = serializers.CharField(
        max_length=models.TOKEN_LENGTH, write_only=True
    )

    _verification: models.EmailVerification = None

    def save(self, **kwargs):
        """
        Mark the email address associated with the token as verified and
        delete the verification token.
        """
        self._verification.verify()

    def validate_token(self, token):
        """
        Validate the provided token.

        Args:
            token:
                The token to validate.

        Returns:
            The provided token if it exists in the database.

        Raises:
            serializers.ValidationError:
                If the token is invalid.
        """
        try:
            self._verification = models.EmailVerification.objects.get(
                token=token
            )
        except models.EmailVerification.DoesNotExist:
            raise serializers.ValidationError(
                _("The provided verification token is invalid.")
            )

        return token


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer to create and send a password reset token to a verified
    email address.
    """

    email = serializers.EmailField()

    def save(self, **kwargs) -> Optional[models.PasswordReset]:
        """
        Send a new password reset token to the provided email address if
        the email has already been verified. If the provided email has
        not been verified, no action is taken.

        Returns:
            The created :py:class:`PasswordReset` instance if one was
            created or else ``None``.
        """
        try:
            email = models.EmailAddress.objects.get(
                address__iexact=self.validated_data["email"], is_verified=True
            )
        except models.EmailAddress.DoesNotExist:
            return None

        reset = models.PasswordReset(email=email)
        reset.send_email()

        return reset


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer to reset a user's password.
    """

    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )
    token = serializers.CharField(
        max_length=models.TOKEN_LENGTH, write_only=True
    )

    _reset: models.PasswordReset = None

    def save(self, **kwargs):
        """
        Reset the password of the user associated with the provided
        password reset token.
        """
        reset = self._reset
        user = reset.email.user
        user.set_password(self.validated_data["password"])
        user.save()

        logger.info("Reset the password for user %r", user)

        reset.delete()

    def validate(self, attrs: dict) -> dict:
        """
        Ensure that the provided token is valid and the provided
        password passes Django's built in password validation.

        Args:
            attrs:
                The data to validate.

        Returns:
            The validated data.
        """
        try:
            self._reset = models.PasswordReset.objects.get(
                token=attrs["token"]
            )
        except models.PasswordReset.DoesNotExist:
            raise serializers.ValidationError(
                {"token": _("The provided password reset token is invalid.")}
            )

        try:
            password_validation.validate_password(
                attrs["password"], user=self._reset.email.user
            )
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        return attrs
