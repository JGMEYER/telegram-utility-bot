import pytest
from unittest import TestCase

from ....service.applemusic import AppleMusic


class TestIntegAppleMusic(TestCase):
    """Integration tests for AppleMusic"""

    @pytest.mark.integ
    def test_applemusic_track_fetch(self):
        """Test ability to fetch tracks"""
        with AppleMusic() as applemusic:
            track = applemusic.search_one_track("Polyphia G.O.A.T.")
            self.assertEqual(track.artist.lower(), "polyphia")
            self.assertEqual(track.title.lower(), "g.o.a.t.")

            # trackId may change, not worth testing this
            trackId = applemusic.get_trackId_from_url(track.share_link())

            track = applemusic.get_track_from_trackId(trackId)
            self.assertEqual(track.artist.lower(), "polyphia")
            self.assertEqual(track.title.lower(), "g.o.a.t.")
