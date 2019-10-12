import pytest
import requests
from django.contrib.auth import get_user_model

from email_auth import models


pytest.importorskip("rest_framework")

from email_auth.interfaces.rest import serializers, views  # noqa


def test_get_serializer_class():
    """
    Test the serializer class used by the view.
    """
    view = views.PasswordResetView()
    expected = serializers.PasswordResetSerializer

    assert view.get_serializer_class() == expected


@pytest.mark.functional_test
def test_reset_password(live_server):
    """
    Sending a ``POST`` request to the endpoint with a valid reset token
    and a valid new password should reset the user's password.
    """
    user = get_user_model().objects.create_user(username="Test User")
    email = models.EmailAddress.objects.create(
        address="test@example.com", is_verified=True, user=user
    )
    reset = models.PasswordReset.objects.create(email=email)

    data = {"password": "NewPassword", "token": reset.token}
    url = f"{live_server}/rest/password-resets/"
    response = requests.post(url, data)

    assert response.status_code == 201
    assert response.json() == {}

    user.refresh_from_db()

    assert user.check_password(data["password"])


@pytest.mark.functional_test
def test_reset_password_invalid_token(live_server):
    """
    Sending a ``POST`` request to the endpoint with an invalid token
    should return a 400 response and not change the user's password.
    """
    password = "password"
    user = get_user_model().objects.create_user(
        password=password, username="Test User"
    )

    data = {"password": password * 2, "token": "invalid-token"}
    url = f"{live_server}/rest/password-resets/"
    response = requests.post(url, data)

    assert response.status_code == 400
    assert response.json() == {
        "token": ["The provided password reset token is invalid."]
    }

    # Password shouldn't have changed
    user.refresh_from_db()
    assert user.check_password(password)
