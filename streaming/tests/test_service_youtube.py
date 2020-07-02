from unittest import TestCase

from ..service_youtube import YouTube


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
