from unittest import mock

import pytest
from django.conf import settings

from email_auth import models


pytest.importorskip("rest_framework")

# Imports that require "rest_framework"
from email_auth.interfaces.rest import serializers  # noqa


@mock.patch("email_auth.models.EmailVerification.send_email")
def test_save_unverified_email(_, mock_email_address_qs):
    """
    Saving the serializer with an address that exists in the database
    but has not yet been verified should send a new verification email
    to the provided address.
    """
    email = models.EmailAddress(address="test@example.com", is_verified=False)
    mock_email_address_qs.get.return_value = email

    data = {"email": email.address}
    serializer = serializers.EmailVerificationRequestSerializer(data=data)

    assert serializer.is_valid()
    verification = serializer.save()

    assert mock_email_address_qs.get.call_args[1] == {
        "address__iexact": email.address
    }
    assert verification.email == email
    assert verification.send_email.call_count == 1


@mock.patch("email_auth.models.EmailAddress.send_already_verified")
def test_save_verified_email(_, mock_email_address_qs):
    """
    Saving the serializer with an email address that has already been
    verified should send the user a notification that their email has
    already been verified.
    """
    email = models.EmailAddress(address="test@example.com", is_verified=True)
    mock_email_address_qs.get.return_value = email

    data = {"email": email.address}
    serializer = serializers.EmailVerificationRequestSerializer(data=data)

    assert serializer.is_valid()
    verification = serializer.save()

    assert mock_email_address_qs.get.call_args[1] == {
        "address__iexact": email.address
    }
    assert verification is None
    assert email.send_already_verified.call_count == 1


@mock.patch("email_auth.interfaces.rest.serializers.email_utils.send_email")
def test_save_missing_email(mock_send_email, mock_email_address_qs):
    """
    If the provided email doesn't exist in the database, an email should
    be sent telling the user to register or add the email address to
    their account.
    """
    mock_email_address_qs.get.side_effect = models.EmailAddress.DoesNotExist

    data = {"email": "test@example.com"}
    serializer = serializers.EmailVerificationRequestSerializer(data=data)

    assert serializer.is_valid()
    verification = serializer.save()

    assert mock_email_address_qs.get.call_args[1] == {
        "address__iexact": data["email"]
    }
    assert verification is None
    assert mock_send_email.call_args[1] == {
        "context": {"email": data["email"]},
        "from_email": settings.DEFAULT_FROM_EMAIL,
        "recipient_list": [data["email"]],
        "subject": "Unregistered Email Address",
        "template_name": "email_auth/emails/unregistered-email",
    }
