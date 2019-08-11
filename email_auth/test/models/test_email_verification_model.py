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


def test_str():
    """
    Converting a verification instance to a string should return a
    message stating which email address the verification is for.
    """
    email = models.EmailAddress(address="test@example.com")
    verification = models.EmailVerification(email=email)
    expected = f"Verification for {email}"

    assert str(verification) == expected
