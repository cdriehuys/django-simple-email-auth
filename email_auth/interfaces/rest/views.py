from rest_framework import generics

from email_auth.interfaces.rest import serializers


class EmailVerificationView(generics.CreateAPIView):
    """
    post:
    Verify ownership of an email address using a verification token.

    If the provided token is valid, a `201` response is returned.

    If the provided token is invalid, a `400` response containing an
    error message is returned.
    """

    serializer_class = serializers.EmailVerificationSerializer
