import logging

from django.contrib.auth import get_user_model

from email_auth import models


logger = logging.getLogger(__name__)


class VerifiedEmailBackend:
    """
    Authentication backend that allows users to authenticate with any
    email address they have verified ownership of.
    """

    def authenticate(self, request, username=None, password=None):
        """
        Attempt to authenticate a user.

        Args:
            request:
                The request that initiated the authentication process.
            username:
                The user's identifier. In this case, any email address
                that they own.
            password:
                The user's password.

        Returns:
            The user matching the provided credentials if they exist or
            ``None`` if they don't.
        """
        try:
            email = models.EmailAddress.objects.get(
                address=username, is_verified=True
            )
        except models.EmailAddress.DoesNotExist:
            # Do a password comparison anyway to mitigate timing
            # attacks.
            dummy_user = get_user_model()
            dummy_user.set_password("jekyll")
            dummy_user.check_password("hyde")

            logger.debug("Could not find verified email: %s", username)
            return None

        if email.user.check_password(password) and email.user.is_active:
            logger.debug(
                "Authenticated user with email '%s': %r", username, email.user
            )
            return email.user

        return None

    def get_user(self, user_id):
        """
        Get a user by their ID.

        Args:
            user_id:
                The ID of the user to retrieve.

        Returns:
            The user with the specified ID or ``None`` if there is no
            user with the provided ID.
        """
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
