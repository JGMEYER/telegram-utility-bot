from unittest import TestCase

from ...service.gmusic import GMusic


class TestGMusic(TestCase):
    """GMusic tests"""

    def test_supports_track_url(self):
        """Tests for supports_track_url method"""
        self.assertTrue(
            GMusic.supports_track_url(
                "https://play.google.com/music/m/T2y24nzjhuyvlolsptj7zqon5qi"
            )
        )
        self.assertTrue(
            GMusic.supports_track_url(
                "https://play.google.com/music/m/T2y24nzjhuyvlolsptj7zqon5qi?t=GOAT_-_Polyphia"  # noqa: E501
            )
        )
        self.assertFalse(
            GMusic.supports_track_url("https://play.google.com/music/m/")
        )

    def test_get_trackId_from_url(self):
        """Tests for get_trackId_from_url method"""
        self.assertEqual(
            GMusic.get_trackId_from_url(
                "https://play.google.com/music/m/T2y24nzjhuyvlolsptj7zqon5qi?t=GOAT_-_Polyphia"  # noqa: E501
            ),
            "T2y24nzjhuyvlolsptj7zqon5qi",
        )
