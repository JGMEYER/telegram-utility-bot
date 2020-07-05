import pytest
from unittest import TestCase

from ....service.spotify import Spotify


class TestIntegSpotify(TestCase):
    """Integration tests for Spotify"""

    @pytest.mark.integ
    def test_spotify_track_fetch(self):
        """Test ability to fetch tracks"""
        with Spotify() as spotify:
            track = spotify.search_one_track("G.O.A.T. Polyphia")
            self.assertEqual(track.name.lower(), "g.o.a.t.")
            self.assertEqual(track.artist.lower(), "polyphia")

            # trackId may change, not worth testing this
            trackId = spotify.get_trackId_from_url(track.share_link())

            track = spotify.get_track_from_trackId(trackId)
            self.assertEqual(track.name.lower(), "g.o.a.t.")
            self.assertEqual(track.artist.lower(), "polyphia")
