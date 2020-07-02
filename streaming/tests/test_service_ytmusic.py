from unittest import TestCase

from ..service_ytmusic import YTMusic


class TestYTMusic(TestCase):
    """YTMusic tests"""

    def test_supports_track_url(self):
        """Tests for supports_track_url method"""
        self.assertTrue(
            YTMusic.supports_track_url(
                "https://music.youtube.com/watch?v=2hln1TOQUZ0"
            )
        )
        self.assertTrue(
            YTMusic.supports_track_url(
                "https://music.youtube.com/watch?v=2hln1TOQUZ0&list=RDAMVM2hln1TOQUZ0"  # noqa: E501
            )
        )
        self.assertFalse(
            YTMusic.supports_track_url("https://music.youtube.com/")
        )

    def test_get_trackId_from_url(self):
        """Tests for get_trackId_from_url"""
        self.assertEqual(
            YTMusic.get_trackId_from_url(
                "https://music.youtube.com/watch?v=2hln1TOQUZ0",
            ),
            "2hln1TOQUZ0",
        )
        self.assertEqual(
            YTMusic.get_trackId_from_url(
                "https://music.youtube.com/watch?v=2hln1TOQUZ0&list=RDAMVM2hln1TOQUZ0",  # noqa: E501
            ),
            "2hln1TOQUZ0",
        )
