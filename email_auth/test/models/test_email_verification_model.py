from unittest import mock

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from email_auth import models
from email_auth.test import test_utils


def test_init_all_fields():
    """
    Test creating an email verification with all allowed fields.
    """
    verification = models.EmailVerification(
        email=models.EmailAddress(), time_sent=timezone.now()
    )

    assert verification.pk


def test_repr():
    """
    The string representation of an instance should contain all the
    information necessary to recreate it.
    """
    email = models.EmailAddress(
        address="test@example.com", user=get_user_model()()
    )
    verification = models.EmailVerification(
        email=email, time_sent=timezone.now()
    )
    expected = test_utils.create_expected_repr(
        verification,
        ["email", "time_created", "time_sent", "time_updated", "token"],
    )

    assert repr(verification) == expected


@mock.patch("email_auth.models.email_utils.send_email", autospec=True)
def test_send_email(mock_send_email):
    """
    Sending an email should use django-email-utils to send the
    verification token to the user.
    """
    user = get_user_model()()
    email = models.EmailAddress(address="test@example.com", user=user)
    verification = models.EmailVerification(email=email)

    verification.send_email()

    assert mock_send_email.call_args[1] == {
        "context": {
            "email": email,
            "user": user,
            "verification": verification,
        },
        "from_email": settings.DEFAULT_FROM_EMAIL,
        "recipient_list": [email.address],
        "subject": "Please Verify Your Email Address",
        "template_name": "email_auth/emails/verify-email",
    }


def test_str():
    """
    Converting a verification instance to a string should return a
    message stating which email address the verification is for.
    """
    email = models.EmailAddress(address="test@example.com")
    verification = models.EmailVerification(email=email)
    expected = f"Verification for {email}"

    assert str(verification) == expected
