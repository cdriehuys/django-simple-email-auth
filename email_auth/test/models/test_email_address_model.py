from unittest import mock

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
        normalized_address="test@example.com",
        time_verified=timezone.now(),
        user=auth.get_user_model()(),
    )

    # Default fields should be populated
    assert email.pk


def test_clean_normalize_email_address():
    """
    Cleaning an email address should populate the "normalized" field
    with a lower-cased version of the address.
    """
    email = models.EmailAddress(address="TeSt@ExAmPlE.cOm")

    email.clean()

    assert email.normalized_address == email.address.lower()


def test_repr():
    """
    The string representation of an email address should contain all
    the information needed to reconstruct the instance.
    """
    email = models.EmailAddress(
        address="test@example.com",
        normalized_address="test@example.com",
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
            "normalized_address",
            "time_created",
            "time_updated",
            "time_verified",
            "user",
        ],
    )

    assert repr(email) == expected


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
