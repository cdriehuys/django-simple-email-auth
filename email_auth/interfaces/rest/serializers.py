from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from email_auth import models


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
