import json

import pytest
from unittest import TestCase

import handler
from utils.env import getenv

TELEGRAM_CHAT_ID = getenv("TELEGRAM_CHAT_ID")


class TestIntegHandler(TestCase):
    """Integration tests for handler.py"""

    @pytest.mark.integ
    def test_handle_webhook_update_search(self):
        """Integration test for handle_webhook_update method.

        Posts message to TELEGRAM_CHAT_ID.
        """
        text = "@BopizTestBot volbeat - lola montez"
        event = {
            "body": json.dumps(
                {
                    "update_id": 10000,
                    "message": {
                        "date": 99999999999,
                        "chat": {
                            "last_name": "Test Lastname",
                            "id": TELEGRAM_CHAT_ID,
                            "first_name": "Test",
                            "username": "Test",
                        },
                        "message_id": 1365,
                        "from": {
                            "last_name": "Test Lastname",
                            "id": 1111111,
                            "first_name": "Test",
                            "username": "Test",
                        },
                        "text": text,
                    },
                }
            )
        }
        response = handler.handle_webhook_update(event, None)
        self.assertEqual(response["statusCode"], 200)

    @pytest.mark.integ
    def test_handle_webhook_update_mirror_links(self):
        """Integration test for handle_webhook_update method.

        Posts message to TELEGRAM_CHAT_ID.
        """
        text = (
            "handler.handle_webhook_update() integration test:\n"
            "https://play.google.com/music/m/Tkqhlm2ssr4y2s76wfcjahkv3b4\n"  # no longer supported
            "https://open.spotify.com/track/1wnq9TwifJ9ipLUFsm8vKx?si=IUytRONLTYWxJz3g5L9y8g\n"  # noqa: E501
            "https://youtu.be/_kvZpVMY89c\n"
            "https://youtu.be/srre8i83vL8\n"  # non-music link
            "https://music.youtube.com/watch?v=xsKQdGkrqkw&feature=share"
        )
        event = {
            "body": json.dumps(
                {
                    "update_id": 10000,
                    "message": {
                        "date": 99999999999,
                        "chat": {
                            "last_name": "Test Lastname",
                            "id": TELEGRAM_CHAT_ID,
                            "first_name": "Test",
                            "username": "Test",
                        },
                        "message_id": 1365,
                        "from": {
                            "last_name": "Test Lastname",
                            "id": 1111111,
                            "first_name": "Test",
                            "username": "Test",
                        },
                        "text": text,
                    },
                }
            )
        }
        response = handler.handle_webhook_update(event, None)
        self.assertEqual(response["statusCode"], 200)
