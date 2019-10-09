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
