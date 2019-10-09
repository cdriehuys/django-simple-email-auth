import pytest
import requests
from django.contrib.auth import get_user_model

from email_auth import models


pytest.importorskip("rest_framework")

# Imports that require "rest_framework"
from email_auth.interfaces.rest import views, serializers  # noqa


def test_get_serializer_class():
    """
    Test the serializer class used by the view.
    """
    view = views.EmailVerificationRequestView()
    expected = serializers.EmailVerificationRequestSerializer

    assert view.get_serializer_class() == expected


@pytest.mark.functional_test
def test_request_verification_email(live_server, mailoutbox, settings):
    """
    Sending a ``POST`` request to the endpoint with an unverified email
    address should send an email with a new verification token to the
    user.
    """
    url_template = "https://localhost/verify-email/{key}"
    settings.EMAIL_AUTH = {"EMAIL_VERIFICATION_URL": url_template}

    user = get_user_model().objects.create_user(username="test-user")
    email = models.EmailAddress.objects.create(
        address="test@example.com", user=user
    )

    data = {"email": email.address}
    url = f"{live_server}/rest/email-verification-requests/"
    response = requests.post(url, data)

    assert response.status_code == 201
    assert response.json() == data
    assert len(mailoutbox) == 1

    msg = mailoutbox[0]

    assert msg.to == [email.address]
    assert url_template.format(key=email.verifications.get().token) in msg.body


@pytest.mark.functional_test
def test_request_verification_email_already_verified(live_server, mailoutbox):
    """
    Sending a ``POST`` request to the endpoint with a verified email
    address should send an email notifying the user the email is already
    registered.
    """
    user = get_user_model().objects.create_user(username="test-user")
    email = models.EmailAddress.objects.create(
        address="test@example.com", is_verified=True, user=user
    )

    data = {"email": email.address}
    url = f"{live_server}/rest/email-verification-requests/"
    response = requests.post(url, data)

    assert response.status_code == 201
    assert response.json() == data
    assert len(mailoutbox) == 1

    msg = mailoutbox[0]

    assert msg.to == [email.address]
    assert "already been verified" in msg.subject.lower()


@pytest.mark.functional_test
def test_request_verification_email_unknown_address(live_server, mailoutbox):
    """
    Sending a ``POST`` request to the endpoint with an unknown email
    address should send an email notifying the user their email address
    has not been registered yet.
    """
    data = {"email": "unknown@example.com"}
    url = f"{live_server}/rest/email-verification-requests/"
    response = requests.post(url, data)

    assert response.status_code == 201
    assert response.json() == data
    assert len(mailoutbox) == 1

    msg = mailoutbox[0]

    assert msg.to == [data["email"]]
    assert "unregistered email" in msg.subject.lower()
