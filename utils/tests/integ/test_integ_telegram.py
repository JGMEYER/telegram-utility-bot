import pytest
from unittest import TestCase

from ... import telegram
from utils.env import getenv


class TestIntegTelegram(TestCase):
    """Integration tests for telegram.py"""

    def setUp(self):
        """Set up test variables"""
        self.telegram_token = getenv("TELEGRAM_TOKEN")
        self.telegram_chat_id = getenv("TELEGRAM_CHAT_ID")

    @pytest.mark.integ
    def test_send_message(self):
        """Test send_message() function"""
        text = "`telegram.send_message()` integration test"
        response = telegram.send_message(
            self.telegram_token, self.telegram_chat_id, text
        )
        self.assertEqual(response["statusCode"], 200)
