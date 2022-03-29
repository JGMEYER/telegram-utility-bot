from unittest import TestCase

from ... import telegram


class TestTelegram(TestCase):
    """Telegram tests"""

    def test_get_api_url(self):
        mock_bot_id = "0123456789"
        mock_api_key = "fake-auth"
        mock_token = f"{mock_bot_id}:{mock_api_key}"

        api_url = telegram.get_api_url(mock_token)
        self.assertEqual(
            api_url, f"https://api.telegram.org/bot0123456789:fake-auth/"
        )

    def test_get_mentions_from_text(self):
        text = "@username hello world @other goodnight moon"
        entities = [
            {"offset": 0, "length": 9, "type": "mention"},
            {"offset": 22, "length": 6, "type": "mention"},
        ]

        actual = telegram.get_mentions_from_text(text, entities)
        expected = ["@username", "@other"]
        self.assertEqual(actual, expected)
