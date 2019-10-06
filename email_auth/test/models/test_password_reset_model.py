from unittest import mock

from django.conf import settings as django_settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from email_auth import models
from email_auth.test import test_utils


def test_init_with_all_fields():
    """
    Test creating a new password reset with all fields that aren't
    automatically populated.
    """
    password_reset = models.PasswordReset(email=models.EmailAddress())

    assert password_reset.pk
    assert password_reset.token


def test_repr():
    """
    The string representation of a token should contain all the fields
    required to reconstruct it.
    """
    user = get_user_model()()
    email = models.EmailAddress(user=user)
    password_reset = models.PasswordReset(
        email=email,
        time_created=timezone.now(),
        time_sent=timezone.now(),
        time_updated=timezone.now(),
    )
    expected = test_utils.create_expected_repr(
        password_reset,
        ["email", "time_created", "time_sent", "time_updated", "token"],
    )

    assert repr(password_reset) == expected


@mock.patch("email_auth.models.PasswordReset.save", autospec=True)
@mock.patch("email_auth.models.email_utils.send_email", autospec=True)
@mock.patch("email_auth.models.timezone.now", autospec=True)
def test_send_email(mock_now, mock_send_email, _):
    """
    This method should send the password reset token to the associated
    email address and record the send time of the email.
    """
    email = models.EmailAddress(address="test@example.com")
    password_reset = models.PasswordReset(email=email)

    password_reset.send_email()

    assert mock_send_email.call_args[1] == {
        "context": {"password_reset": password_reset, "reset_url": None},
        "from_email": django_settings.DEFAULT_FROM_EMAIL,
        "recipient_list": [email.address],
        "subject": "Reset Your Password",
        "template_name": "email_auth/emails/reset-password",
    }

    assert password_reset.time_sent == mock_now.return_value
    assert password_reset.save.call_count == 1


@mock.patch("email_auth.models.PasswordReset.save", autospec=True)
@mock.patch("email_auth.models.email_utils.send_email", autospec=True)
@mock.patch("email_auth.models.timezone.now", autospec=True)
def test_send_email_with_reset_url(mock_now, mock_send_email, _, settings):
    """
    This method should send the password reset token to the associated
    email address and record the send time of the email.
    """
    reset_url_template = "example.com/reset-password/{key}"
    settings.EMAIL_AUTH = {"PASSWORD_RESET_URL": reset_url_template}

    email = models.EmailAddress(address="test@example.com")
    password_reset = models.PasswordReset(email=email)

    password_reset.send_email()

    assert mock_send_email.call_args[1] == {
        "context": {
            "password_reset": password_reset,
            "reset_url": reset_url_template.format(key=password_reset.token),
        },
        "from_email": django_settings.DEFAULT_FROM_EMAIL,
        "recipient_list": [email.address],
        "subject": "Reset Your Password",
        "template_name": "email_auth/emails/reset-password",
    }

    assert password_reset.time_sent == mock_now.return_value
    assert password_reset.save.call_count == 1


def test_str():
    """
    Converting a password reset to a string should return a message
    including the email address the token is associated with.
    """
    email = models.EmailAddress(address="test@example.com")
    password_reset = models.PasswordReset(email=email)
    expected = f"Password reset for '{email}'"

    assert str(password_reset) == expected
