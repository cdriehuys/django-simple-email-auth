from unittest import mock

from django.conf import settings
from django.contrib import auth
from django.utils import timezone

from email_auth import models
from email_auth.test import test_utils


def test_init_with_all_fields():
    """
    Test the fields allowed for an email address.
    """
    email = models.EmailAddress(
        address="Test@Example.com",
        is_verified=True,
        time_verified=timezone.now(),
        user=auth.get_user_model()(),
    )

    # Default fields should be populated
    assert email.pk


def test_repr():
    """
    The string representation of an email address should contain all
    the information needed to reconstruct the instance.
    """
    email = models.EmailAddress(
        address="test@example.com",
        time_created=timezone.now(),
        time_updated=timezone.now(),
        time_verified=timezone.now(),
        user=auth.get_user_model()(),
    )
    expected = test_utils.create_expected_repr(
        email,
        [
            "address",
            "id",
            "is_verified",
            "time_created",
            "time_updated",
            "time_verified",
            "user",
        ],
    )

    assert repr(email) == expected


@mock.patch("email_auth.models.email_utils.send_email", autospec=True)
def test_send_already_verified(mock_send_email):
    """
    This method should send a notification to the email address letting
    the user know their email address is already verified.
    """
    email = models.EmailAddress(address="test@example.com")
    email.send_already_verified()

    assert mock_send_email.call_args[1] == {
        "context": {"email": email},
        "from_email": settings.DEFAULT_FROM_EMAIL,
        "recipient_list": [email.address],
        "subject": "Your Email Address has Already Been Verified",
        "template_name": "email_auth/emails/already-verified",
    }


@mock.patch("email_auth.models.email_utils.send_email", autospec=True)
def test_send_duplicate_notification(mock_send_email):
    """
    This method should send a notification to the email address letting
    the user know another attempt was made to register the email
    address.
    """
    email = models.EmailAddress(address="test@example.com")
    email.send_duplicate_notification()

    assert mock_send_email.call_args[1] == {
        "context": {"email": email},
        "from_email": settings.DEFAULT_FROM_EMAIL,
        "recipient_list": [email.address],
        "subject": "Your Email Address has Already Been Registered",
        "template_name": "email_auth/emails/duplicate-email",
    }


@mock.patch("email_auth.models.EmailVerification.save", autospec=True)
@mock.patch("email_auth.models.EmailVerification.send_email", autospec=True)
def test_send_verification_email(*_):
    """
    This method should create a new verification token for the address
    and send it to the user.
    """
    email = models.EmailAddress(address="test@example.com")
    verification = email.send_verification_email()

    assert verification.save.call_count == 1
    assert verification.send_email.call_count == 1


def test_str():
    """
    Converting an email address to a string should return the address
    text as specified by the owner.
    """
    email = models.EmailAddress(address="Test@Example.com")

    assert str(email) == email.address


@mock.patch("email_auth.models.timezone.now", return_value=timezone.now())
def test_verify(mock_now):
    email = models.EmailAddress()

    with mock.patch.object(email, "save", autospec=True) as mock_save:
        email.verify()

    assert email.is_verified
    assert email.time_verified == mock_now.return_value
    assert mock_save.call_count == 1
