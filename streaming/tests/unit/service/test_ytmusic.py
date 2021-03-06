from unittest import TestCase

from ....service.ytmusic import YTMusic


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
        # dash in trackId
        self.assertTrue(
            YTMusic.supports_track_url(
                "https://music.youtube.com/watch?v=4KBf-DPKA2U&feature=share"
            )
        )
        # underscore in trackId
        self.assertTrue(
            YTMusic.supports_track_url(
                "https://music.youtube.com/watch?v=5WQN2Ecz_ME&list=RDAMVM5WQN2Ecz_ME"  # noqa: E501
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
        # dash in trackId
        self.assertEqual(
            YTMusic.get_trackId_from_url(
                "https://music.youtube.com/watch?v=4KBf-DPKA2U&feature=share"
            ),
            "4KBf-DPKA2U",
        )
        # underscore in trackId
        self.assertEqual(
            YTMusic.get_trackId_from_url(
                "https://music.youtube.com/watch?v=5WQN2Ecz_ME&list=RDAMVM5WQN2Ecz_ME"  # noqa: E501
            ),
            "5WQN2Ecz_ME",
        )
