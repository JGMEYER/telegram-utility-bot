import pytest

from ... import match
from ...service.spotify import Spotify, SpotifyTrack
from ...service.youtube import YouTube, YouTubeTrack
from ...service.ytmusic import YTMusic, YTMusicTrack


@pytest.mark.integ
@pytest.mark.slow
def test_get_similar_track_for_original_track():
    """Tests for get_similar_track_for_original_track() function.

    Use examples from prior failed cases.
    """

    def _assert_matches_all_services(track_svc, title, artist):
        track_type = None
        if track_svc == Spotify:
            track_type = SpotifyTrack
        elif track_svc == YouTube:
            track_type = YouTubeTrack
        elif track_svc == YTMusic:
            track_type = YTMusicTrack
        else:
            raise Exception("SVC not supported by test")

        track = track_type(title, artist, None)
        similar_tracks = match.get_similar_tracks_for_original_track(
            track_svc, track
        )

        print(similar_tracks.values())
        assert all(similar_tracks.values())
        # We want this to fail when adding new svcs, for visibility
        assert len(similar_tracks.keys()) == 2

    # Spotify

    _assert_matches_all_services(Spotify, "Blood Bank", "Bon Iver")

    # YouTube

    _assert_matches_all_services(
        YouTube, "Bon Iver - PDLIF - Official Video", "Bon Iver"
    )
    # Video actually separates title and artist
    _assert_matches_all_services(
        YouTube, "Patterns (Demo)", "Letters To The Editor - Topic"
    )

    # YTMusic

    _assert_matches_all_services(
        YTMusic, "Save Me (New Unreleased Video)", "Jelly Roll"
    )
