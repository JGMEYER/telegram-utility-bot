import pytest
from unittest import TestCase

from ....service.gmusic import GMusic


class TestIntegGMusic(TestCase):
    """Integration tests for GMusic"""

    @pytest.mark.integ
    def test_gmusic_fetch(self):
        with GMusic() as gm:
            track = gm.search_one_track("G.O.A.T. Polyphia")
            self.assertEqual(track.name.lower(), "g.o.a.t.")
            self.assertEqual(track.artist.lower(), "polyphia")

            # trackId may change, not worth testing this
            trackId = GMusic.get_trackId_from_url(track.share_link())

            track = gm.get_track_from_trackId(trackId)
            self.assertEqual(track.name.lower(), "g.o.a.t.")
            self.assertEqual(track.artist.lower(), "polyphia")
