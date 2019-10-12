from unittest import mock

import pytest

from email_auth import models


pytest.importorskip("rest_framework")

# Imports that require the presence of "rest_framework"
from email_auth.interfaces.rest import serializers  # noqa


def test_save_unregistered_email(mock_email_address_qs):
    """
    If the provided email address doesn't exist in the system, saving
    should do nothing.
    """
    address = "test@example.com"
    mock_email_address_qs.get.side_effect = models.EmailAddress.DoesNotExist

    data = {"email": address}
    serializer = serializers.PasswordResetRequestSerializer(data=data)

    assert serializer.is_valid()
    result = serializer.save()

    assert result is None
    assert serializer.data == data
    assert mock_email_address_qs.get.call_args[1] == {
        "address__iexact": address,
        "is_verified": True,
    }


def test_save_unverified_email(mock_email_address_qs):
    """
    If the provided email address has not been verified yet, saving the
    serializer should do nothing.
    """
    address = "test@example.com"
    mock_email_address_qs.get.side_effect = models.EmailAddress.DoesNotExist

    data = {"email": address}
    serializer = serializers.PasswordResetRequestSerializer(data=data)

    assert serializer.is_valid()
    result = serializer.save()

    assert result is None
    assert serializer.data == data
    assert mock_email_address_qs.get.call_args[1] == {
        "address__iexact": address,
        "is_verified": True,
    }


@mock.patch("email_auth.models.PasswordReset.send_email")
def test_save_verified_email(_, mock_email_address_qs):
    """
    If a verified email is provided, saving the serializer should send
    a new password reset token to the provided address.
    """
    email = models.EmailAddress(address="test@example.com")
    mock_email_address_qs.get.return_value = email

    data = {"email": email.address}
    serializer = serializers.PasswordResetRequestSerializer(data=data)

    assert serializer.is_valid()
    result = serializer.save()

    assert serializer.data == data
    assert result.send_email.call_count == 1
    assert mock_email_address_qs.get.call_args[1] == {
        "address__iexact": email.address,
        "is_verified": True,
    }
