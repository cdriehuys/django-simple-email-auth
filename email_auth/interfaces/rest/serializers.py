from typing import Optional

import email_utils
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from email_auth import models


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
