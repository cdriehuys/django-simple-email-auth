import string
from unittest import mock

from email_auth import models


@mock.patch("email_auth.models.crypto.get_random_string", autospec=True)
def test_generate_token(mock_random_string):
    """
    The generation function should use Django's cryptography utilities
    to generate a random alphanumeric string.
    """
    char_set = set(string.ascii_letters + string.digits)

    result = models.generate_token()

    assert result == mock_random_string.return_value
    assert set(mock_random_string.call_args[1]["allowed_chars"]) == char_set
    assert mock_random_string.call_args[1]["length"] == 64
