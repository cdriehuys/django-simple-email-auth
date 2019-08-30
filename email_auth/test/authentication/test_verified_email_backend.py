from unittest import mock

import pytest
from django.contrib.auth import get_user_model

from email_auth import authentication, models


@pytest.fixture
def mock_email_address_qs():
    mock_qs = mock.Mock(spec=models.EmailAddress.objects)
    mock_qs.all.return_value = mock_qs

    with mock.patch("email_auth.models.EmailAddress.objects", new=mock_qs):
        yield mock_qs


@pytest.fixture
def mock_user_qs():
    mock_qs = mock.Mock(spec=get_user_model().objects)
    mock_qs.all.return_value = mock_qs

    with mock.patch("django.contrib.auth.models.User.objects", new=mock_qs):
        yield mock_qs


def test_authenticate_with_verified_email_correct_password(
    mock_email_address_qs
):
    """
    If a verified email address and the password of the user who owns
    the email address are provided, the authentication method should
    return the owner of the email address.
    """
    password = "password"
    user = get_user_model()(is_active=True)
    user.set_password(password)
    email = models.EmailAddress(address="test@example.com", user=user)
    mock_email_address_qs.get.return_value = email

    backend = authentication.VerifiedEmailBackend()

    authenticated_user = backend.authenticate(None, email.address, password)

    assert authenticated_user == user
    assert mock_email_address_qs.get.call_args[1]["address"] == email.address


@mock.patch("email_auth.authentication.get_user_model")
def test_authenticate_with_missing_email(mock_get_user, mock_email_address_qs):
    """
    If no verified email with the given address exists, authentication
    should fail.
    """
    email = "test@example.com"
    mock_email_address_qs.get.side_effect = models.EmailAddress.DoesNotExist

    backend = authentication.VerifiedEmailBackend()
    authenticated_user = backend.authenticate(None, email, "password")

    assert authenticated_user is None
    assert mock_email_address_qs.get.call_args[1]["address"] == email
    assert mock_email_address_qs.get.call_args[1]["is_verified"]

    # There should still be a password check even if no user is found.
    assert mock_get_user.return_value.check_password.call_count == 1


def test_authenticate_with_verified_email_incorrect_password(
    mock_email_address_qs
):
    """
    If the user provides a verified email address but the provided
    password does not match the owner of the email address,
    authentication should fail.
    """
    password = "password"
    user = get_user_model()(is_active=True)
    user.set_password(password + "invalid")
    email = models.EmailAddress(address="test@example.com", user=user)
    mock_email_address_qs.get.return_value = email

    backend = authentication.VerifiedEmailBackend()
    authenticated_user = backend.authenticate(None, email.address, password)

    assert authenticated_user is None


def test_authenticate_with_verified_email_correct_password_inactive_user(
    mock_email_address_qs
):
    """
    If the user provides valid credentials but is inactive,
    authentication should fail.
    """
    password = "password"
    user = get_user_model()(is_active=False)
    user.set_password(password)
    email = models.EmailAddress(address="test@example.com", user=user)
    mock_email_address_qs.get.return_value = email

    backend = authentication.VerifiedEmailBackend()
    authenticated_user = backend.authenticate(None, email.address, password)

    assert authenticated_user is None


def test_get_user(mock_user_qs):
    """
    The authentication backend should allow for fetching a user by their
    ID.
    """
    pk = 42
    user = get_user_model()(pk=pk)
    mock_user_qs.get.return_value = user

    backend = authentication.VerifiedEmailBackend()
    retrieved_user = backend.get_user(pk)

    assert retrieved_user == user
    assert mock_user_qs.get.call_args[1]["pk"] == pk


def test_get_user_invalid_id(mock_user_qs):
    """
    If there is no user with the specified ID, ``None`` should be
    returned.
    """
    mock_user_qs.get.side_effect = get_user_model().DoesNotExist

    backend = authentication.VerifiedEmailBackend()
    retrieved_user = backend.get_user(42)

    assert retrieved_user is None
    assert mock_user_qs.get.call_args[1] == {"pk": 42}
