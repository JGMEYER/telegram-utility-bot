from unittest import TestCase

from ... import telegram


class TestTelegram(TestCase):
    """Telegram tests"""

    def test_get_api_url(self):
        """Tests for get_api_url() method"""
        mock_bot_id = "0123456789"
        mock_api_key = "fake-auth"
        mock_token = f"{mock_bot_id}:{mock_api_key}"

        api_url = telegram.get_api_url(mock_token)
        self.assertEqual(
            api_url, f"https://api.telegram.org/bot0123456789:fake-auth/"
        )
