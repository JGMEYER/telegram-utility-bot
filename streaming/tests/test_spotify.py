from unittest import TestCase

from ..spotify import Spotify


class TestSpotify(TestCase):
    """Spotify tests"""

    def test_supports_track_url(self):
        """Tests for supports_track_url method"""
        self.assertTrue(
            Spotify.supports_track_url(
                "https://open.spotify.com/track/3h3pOvw6hjOvZxRUseB7h9"
            )
        )
        self.assertTrue(
            Spotify.supports_track_url(
                "https://open.spotify.com/track/3h3pOvw6hjOvZxRUseB7h9?si=Ci-fm4N2TYq7kKlJANDnhA"  # noqa: E501
            )
        )
        self.assertFalse(
            Spotify.supports_track_url("https://open.spotify.com/track/")
        )

    def test_get_trackId_from_url(self):
        """Tests for get_trackId_from_url method"""
        self.assertEqual(
            Spotify.get_trackId_from_url(
                "https://open.spotify.com/track/3h3pOvw6hjOvZxRUseB7h9?si=Ci-fm4N2TYq7kKlJANDnhA"  # noqa: E501
            ),
            "3h3pOvw6hjOvZxRUseB7h9",
        )
