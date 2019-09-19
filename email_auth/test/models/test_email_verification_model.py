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


@mock.patch("email_auth.models.EmailVerification.save", autospec=True)
@mock.patch("email_auth.models.email_utils.send_email", autospec=True)
@mock.patch("email_auth.models.timezone.now", autospec=True)
def test_send_email(mock_now, mock_send_email, _):
    """
    This method should send the email verification token to the
    associated email address and record the send time of the email.
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

    assert verification.time_sent == mock_now.return_value
    assert verification.save.call_count == 1


def test_str():
    """
    Converting a verification instance to a string should return a
    message stating which email address the verification is for.
    """
    email = models.EmailAddress(address="test@example.com")
    verification = models.EmailVerification(email=email)
    expected = f"Verification for {email}"

    assert str(verification) == expected


def test_verify():
    """
    Verifying an instance should mark the associated email as verified
    and delete the verification instance.
    """
    email = models.EmailAddress()
    verification = models.EmailVerification(email=email)

    with mock.patch.object(
        email, "verify", autospec=True
    ) as mock_verify, mock.patch.object(
        verification, "delete", autospec=True
    ) as mock_delete:
        verification.verify()

    assert mock_verify.call_count == 1
    assert mock_delete.call_count == 1
