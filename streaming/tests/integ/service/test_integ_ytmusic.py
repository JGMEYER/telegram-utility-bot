import pytest
from unittest import TestCase

from ....service.ytmusic import YTMusic


class TestIntegYTMusic(TestCase):
    """Integration tests for YTMusic"""

    @pytest.mark.integ
    def test_ytmusic_fetch(self):
        """Test ability to fetch tracks"""
        with YTMusic() as ytm:
            track = ytm.search_one_track("G.O.A.T. Polyphia")
            self.assertEqual(track.title.lower(), "g.o.a.t.")
            self.assertEqual(track.artist.lower(), "polyphia")

            # trackId may change, not worth testing this
            trackId = ytm.get_trackId_from_url(track.share_link())

            track = ytm.get_track_from_trackId(trackId)
            self.assertEqual(
                track.searchable_name.lower(), "g.o.a.t. - polyphia"
            )
