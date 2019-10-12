from django.urls import path

from email_auth.interfaces.rest import views


app_name = "email-auth:rest"

urlpatterns = [
    path(
        "email-verification-requests/",
        views.EmailVerificationRequestView.as_view(),
        name="email-verification-request-list",
    ),
    path(
        "email-verifications/",
        views.EmailVerificationView.as_view(),
        name="email-verification-list",
    ),
    path(
        "password-reset-requests/",
        views.PasswordResetRequestView.as_view(),
        name="password-reset-request-list",
    ),
    path(
        "password-resets/",
        views.PasswordResetView.as_view(),
        name="password-reset-list",
    ),
]
