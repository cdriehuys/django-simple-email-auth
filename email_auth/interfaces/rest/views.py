from rest_framework import generics

from email_auth.interfaces.rest import serializers


class EmailVerificationRequestView(generics.CreateAPIView):
    """
    post:
    Request a new verification token be sent to the provided email
    address.

    If the provided email exists in the system but has not been verified
    yet, a new verification token will be generated and sent. If the
    email address does not exist in the system or has already been
    verified, an email describing the situation will be sent instead. In
    any of these cases, a `201` status code is returned.

    If the provided email address is not a valid email, a `400` response
    is returned.
    """

    serializer_class = serializers.EmailVerificationRequestSerializer


class EmailVerificationView(generics.CreateAPIView):
    """
    post:
    Verify ownership of an email address using a verification token.

    If the provided token is valid, a `201` response is returned.

    If the provided token is invalid, a `400` response containing an
    error message is returned.
    """

    serializer_class = serializers.EmailVerificationSerializer


class PasswordResetRequestView(generics.CreateAPIView):
    """
    post:
    Request a password reset token be sent to the provided email
    address.

    If the provided email address exists and is verified, a new password
    reset token will be generated and sent to the provided address. In
    any other case, no email will be sent. Regardless of the outcome, a
    `201` response is returned.

    If the provided email address is not a valid email address, a `400`
    response is returned.
    """

    serializer_class = serializers.PasswordResetRequestSerializer


class PasswordResetView(generics.CreateAPIView):
    """
    post:
    Reset a user's password using a password reset token.

    If the provided token is valid and the new password passes the
    password validation checks, a `201` response is returned and the
    user's password is changed.

    If the provided token is invalid or the new password does not pass
    validation, a `400` response is returned.
    """

    serializer_class = serializers.PasswordResetSerializer
