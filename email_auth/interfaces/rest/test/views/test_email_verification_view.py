import pytest
import requests
from django.contrib.auth import get_user_model

from email_auth import models


pytest.importorskip("rest_framework")

# Imports that require "rest_framework"
from email_auth.interfaces.rest import serializers, views  # noqa


def test_get_serializer_class():
    """
    Test the serializer class used by the view.
    """
    view = views.EmailVerificationView()
    expected = serializers.EmailVerificationSerializer

    assert view.get_serializer_class() == expected


@pytest.mark.functional_test
def test_verify_email(live_server):
    """
    Sending a ``POST`` request to the endpoint with a valid token should
    mark the associated email address as verified.
    """
    user = get_user_model().objects.create_user(username="test")
    email = models.EmailAddress.objects.create(
        address="test@example.com", user=user
    )
    verification = models.EmailVerification.objects.create(email=email)

    data = {"token": verification.token}
    url = f"{live_server}/rest/email-verifications/"
    response = requests.post(url, data)

    assert response.status_code == 201
    assert response.json() == {}


@pytest.mark.functional_test
def test_verify_email_invalid_token(live_server):
    """
    Sending a ``POST`` request to the endpoint with an invalid token
    should return a 400 response.
    """
    data = {"token": "invalid-token"}
    url = f"{live_server}/rest/email-verifications/"
    response = requests.post(url, data)

    assert response.status_code == 400
    assert response.json() == {
        "token": ["The provided verification token is invalid."]
    }
