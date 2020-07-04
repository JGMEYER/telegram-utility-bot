import pytest
from unittest import TestCase

from ....service.ytmusic import YTMusic
from ....streaming import StreamingServiceActionNotSupportedError


class TestIntegYTMusic(TestCase):
    """Integration tests for YTMusic"""

    @pytest.mark.integ
    def test_ytmusic_fetch(self):
        with YTMusic() as ytm:
            track = ytm.search_one_track("G.O.A.T. Polyphia")
            self.assertEqual(track.name.lower(), "g.o.a.t.")
            self.assertEqual(track.artist.lower(), "polyphia")

            # trackId may change, not worth testing this
            trackId = ytm.get_trackId_from_url(track.share_link())

            with self.assertRaises(StreamingServiceActionNotSupportedError):
                track = ytm.get_track_from_trackId(trackId)
