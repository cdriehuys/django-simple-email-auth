from unittest import mock

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from email_auth import models


pytest.importorskip("rest_framework")

from email_auth.interfaces.rest import serializers  # noqa


# Since the serializer uses Django's built in password validators, we
# need a password that will pass them.
NEW_PASSWORD = "MySup3rSecurePassword"


@mock.patch("django.contrib.auth.models.User.save", autospec=True)
@mock.patch("email_auth.models.PasswordReset.delete", autospec=True)
def test_save_valid_token(_, __, mock_password_reset_qs):
    """
    Saving the serializer with a valid token should reset the password
    of the user associated with the reset.
    """
    user = get_user_model()(username="Test User")
    email = models.EmailAddress(user=user)
    reset = models.PasswordReset(email=email)
    mock_password_reset_qs.get.return_value = reset

    data = {"password": NEW_PASSWORD, "token": reset.token}
    serializer = serializers.PasswordResetSerializer(data=data)

    assert serializer.is_valid()
    serializer.save()

    assert serializer.data == {}
    assert user.check_password(NEW_PASSWORD)
    assert mock_password_reset_qs.get.call_args[1] == {"token": reset.token}
    assert user.save.call_count == 1
    assert reset.delete.call_count == 1


@mock.patch(
    "email_auth.interfaces.rest.serializers.password_validation.validate_password",  # noqa
    autospec=True,
    side_effect=ValidationError("Invalid password"),
)
def test_validate(mock_validate_password, mock_password_reset_qs):
    """
    If the provided token is valid, the provided password should be run
    through Django's password validation system.
    """
    user = get_user_model()()
    email = models.EmailAddress(user=user)
    reset = models.PasswordReset(email=email)
    mock_password_reset_qs.get.return_value = reset

    data = {"password": NEW_PASSWORD, "token": reset.token}
    serializer = serializers.PasswordResetSerializer(data=data)

    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {"password"}
    assert mock_password_reset_qs.get.call_args[1] == {"token": reset.token}
    assert mock_validate_password.call_args[0][0] == NEW_PASSWORD
    assert mock_validate_password.call_args[1] == {"user": user}


def test_validate_invalid_token(mock_password_reset_qs):
    """
    If the provided token is not valid, a validation error should be
    raised.
    """
    token = "foo"
    mock_password_reset_qs.get.side_effect = models.PasswordReset.DoesNotExist

    data = {"password": NEW_PASSWORD, "token": token}
    serializer = serializers.PasswordResetSerializer(data=data)

    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {"token"}
