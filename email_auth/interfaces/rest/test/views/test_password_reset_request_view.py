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
    view = views.PasswordResetRequestView()
    expected = serializers.PasswordResetRequestSerializer

    assert view.get_serializer_class() == expected


@pytest.mark.functional_test
def test_request_password_reset(live_server, mailoutbox, settings):
    """
    If the user provides a verified email address to the endpoint, an
    email containing a link to the password reset page should be sent.
    """
    reset_url_template = "http://localhost/reset-password/{key}"
    settings.EMAIL_AUTH = {"PASSWORD_RESET_URL": reset_url_template}

    user = get_user_model().objects.create_user(username="Test User")
    email = models.EmailAddress.objects.create(
        address="test@example.com", is_verified=True, user=user
    )

    data = {"email": email.address}
    url = f"{live_server}/rest/password-reset-requests/"
    response = requests.post(url, data)

    assert response.status_code == 201
    assert response.json() == data
    assert len(mailoutbox) == 1

    msg = mailoutbox[0]
    reset = models.PasswordReset.objects.get()

    assert msg.to == [data["email"]]
    assert reset_url_template.format(key=reset.token) in msg.body


@pytest.mark.functional_test
def test_request_password_reset_missing_email(live_server, mailoutbox):
    """
    If the user provides an email address that does not exist in the
    system, no action should be taken.
    """
    data = {"email": "test@example.com"}
    url = f"{live_server}/rest/password-reset-requests/"
    response = requests.post(url, data)

    assert response.status_code == 201
    assert response.json() == data
    assert len(mailoutbox) == 0


@pytest.mark.functional_test
def test_request_password_reset_unverified_email(live_server, mailoutbox):
    """
    If the user provides an email address that does not exist in the
    system, no action should be taken.
    """
    user = get_user_model().objects.create_user(username="Test User")
    email = models.EmailAddress.objects.create(
        address="test@example.com", is_verified=False, user=user
    )

    data = {"email": email.address}
    url = f"{live_server}/rest/password-reset-requests/"
    response = requests.post(url, data)

    assert response.status_code == 201
    assert response.json() == data
    assert len(mailoutbox) == 0
