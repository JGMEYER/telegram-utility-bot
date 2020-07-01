from unittest import TestCase

from ..google_clients import GMusic, YouTube


class TestYouTube(TestCase):
    """YouTube tests"""

    def test_supports_track_url(self):
        """Tests for supports_track_url method"""
        self.assertTrue(
            YouTube.supports_track_url(
                "https://www.youtube.com/watch?v=GWOIDN-akrY"
            )
        )
        self.assertTrue(
            YouTube.supports_track_url(
                "https://www.youtube.com/watch?v=9_gkpYORQLU"
            )
        )
        self.assertTrue(
            YouTube.supports_track_url(
                "https://www.youtube.com/watch?v=9_gkpYORQLU?t=4"
            )
        )
        self.assertFalse(
            YouTube.supports_track_url("https://www.youtube.com/")
        )
        self.assertTrue(
            YouTube.supports_track_url("https://www.youtu.be/9_gkpYORQLU")
        )
        self.assertTrue(
            YouTube.supports_track_url("https://www.youtu.be/9_gkpYORQLU?t=4")
        )
        self.assertFalse(YouTube.supports_track_url("https://www.youtu.be/"))

    def test_get_trackId_from_url(self):
        """Tests for get_trackId_from_url method"""
        self.assertEqual(
            YouTube.get_trackId_from_url(
                "https://www.youtube.com/watch?v=GWOIDN-akrY"
            ),
            "GWOIDN-akrY",
        )
        self.assertEqual(
            YouTube.get_trackId_from_url(
                "https://www.youtube.com/watch?v=9_gkpYORQLU?t=4"
            ),
            "9_gkpYORQLU",
        )
        self.assertEqual(
            YouTube.get_trackId_from_url(
                "https://www.youtu.be/9_gkpYORQLU?t=4"
            ),
            "9_gkpYORQLU",
        )


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
