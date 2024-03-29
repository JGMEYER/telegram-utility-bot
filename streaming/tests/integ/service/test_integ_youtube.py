import pytest
from unittest import TestCase

from ....service.youtube import YouTube, YouTubeTrack


class TestIntegYouTube(TestCase):
    """Integration tests for YouTube"""

    def _valid_searchable_names(self, artist, title):
        for div in YouTubeTrack.SEARCHABLE_NAME_DIVIDERS:
            yield from [
                f"{title} {div} {artist}".lower(),
                f"{artist} {div} {title}".lower(),
            ]

    @pytest.mark.integ
    def test_youtube_track_fetch(self):
        """Test ability to fetch tracks"""
        with YouTube() as yt:
            track = yt.search_one_track("Polyphia G.O.A.T.")
            self.assertIn(
                track.searchable_name.lower(),
                self._valid_searchable_names("Polyphia", "G.O.A.T."),
            )

            # trackId may change, not worth testing this
            trackId = yt.get_trackId_from_url(track.share_link())

            track = yt.get_track_from_trackId(trackId)
            self.assertIn(
                track.searchable_name.lower(),
                self._valid_searchable_names("Polyphia", "G.O.A.T."),
            )
