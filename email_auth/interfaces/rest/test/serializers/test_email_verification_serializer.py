from unittest import mock

import pytest

from email_auth import models

pytest.importorskip("rest_framework")

# Imports that require "rest_framework"
from rest_framework.exceptions import ValidationError  # noqa

from email_auth.interfaces.rest import serializers  # noqa


@mock.patch("email_auth.models.EmailVerification.verify")
def test_save_valid_data(mock_verify, mock_email_verification_qs):
    """
    Saving a serializer with a valid token should mark the email address
    associated with the token as verified and delete the token.
    """
    verification = models.EmailVerification()
    mock_email_verification_qs.get.return_value = verification

    data = {"token": verification.token}
    serializer = serializers.EmailVerificationSerializer(data=data)

    assert serializer.is_valid()
    serializer.save()

    assert serializer.data == {}
    assert mock_verify.call_count == 1
    assert mock_email_verification_qs.get.call_args[1] == {
        "token": verification.token
    }


def test_validate_valid_token(mock_email_verification_qs):
    """
    If the token is valid, it should be returned.
    """
    verification = models.EmailVerification()
    mock_email_verification_qs.get.return_value = verification
    serializer = serializers.EmailVerificationSerializer()

    token = serializer.validate_token(verification.token)

    assert token == verification.token
    assert mock_email_verification_qs.get.call_args[1] == {
        "token": verification.token
    }


def test_validate_invalid_token(mock_email_verification_qs):
    """
    If the provided token does not match any tokens in the database, a
    ValidationError should be raised.
    """
    token = "invalid"
    mock_email_verification_qs.get.side_effect = (
        models.EmailVerification.DoesNotExist
    )
    serializer = serializers.EmailVerificationSerializer()

    with pytest.raises(ValidationError):
        serializer.validate_token(token)
