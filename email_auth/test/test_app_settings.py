from email_auth import app_settings


def verify_setting_behavior(settings, setting_name, test_value, default=None):
    """
    Verify the behavior of a setting for the scenarios when it is
    provided, is not provided, and when the entire settings dictionary
    is not provided.

    Args:
        settings:
            The settings dictionary to manipulate for the test.
        setting_name:
            The name of the setting to test.
        test_value:
            The value to use when the setting is provided.
        default:
            The expected default value.
    """
    # No settings provided
    if hasattr(settings, "EMAIL_AUTH"):
        del settings.EMAIL_AUTH

    assert getattr(app_settings, setting_name) == default

    # Setting omitted
    settings.EMAIL_AUTH = {}

    assert getattr(app_settings, setting_name) == default

    # Setting provided
    settings.EMAIL_AUTH = {setting_name: test_value}

    assert getattr(app_settings, setting_name) == test_value


def test_email_verification_url(settings):
    """
    Test the behavior of the ``EMAIL_VERIFICATION_URL`` setting.
    """
    verify_setting_behavior(
        settings, "EMAIL_VERIFICATION_URL", "example.com/{key}"
    )


def test_password_reset_url(settings):
    """
    Test the behavior of the ``PASSWORD_RESET_URL`` setting.
    """
    verify_setting_behavior(
        settings, "PASSWORD_RESET_URL", "example.com/{key}"
    )
