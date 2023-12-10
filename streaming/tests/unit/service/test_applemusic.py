from unittest import TestCase

from ....service.applemusic import AppleMusic


class TestAppleMusic(TestCase):
    """Apple Music tests"""

    def test_supports_track_url(self):
        """Tests for supports_track_url method"""
        self.assertTrue(
            AppleMusic.supports_track_url(
                "https://music.apple.com/us/album/snowpoint-city/1541777121?i=1541777214"
            )
        )
        self.assertFalse(
            # album only (not supported)
            AppleMusic.supports_track_url(
                "https://music.apple.com/us/album/snowpoint-city/1541777121"
            )
        )

    def test_get_trackId_from_url(self):
        """Tests for get_trackId_from_url method"""
        self.assertEqual(
            AppleMusic.get_trackId_from_url(
                "https://music.apple.com/us/album/snowpoint-city/1541777121?i=1541777214"
            ),
            "1541777214",
        )
