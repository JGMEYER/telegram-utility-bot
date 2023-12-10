import pytest

from ... import match
from ...service.applemusic import AppleMusic, AppleMusicTrack
from ...service.spotify import Spotify, SpotifyTrack
from ...service.youtube import YouTube, YouTubeTrack
from ...service.ytmusic import YTMusic, YTMusicTrack


@pytest.mark.integ
@pytest.mark.slow
def test_get_similar_track_for_original_track():
    """Tests for get_similar_track_for_original_track() function.

    Use examples from prior failed cases.
    """

    def _assert_matches_all_services(track_svc, artist, title):
        if track_svc == AppleMusic:
            track_type = AppleMusicTrack
        elif track_svc == Spotify:
            track_type = SpotifyTrack
        elif track_svc == YouTube:
            track_type = YouTubeTrack
        elif track_svc == YTMusic:
            track_type = YTMusicTrack
        else:
            track_type = match.SearchTrack

        track = track_type(artist, title, None)
        similar_tracks = match.get_similar_tracks_for_original_track(
            track_svc, track
        )

        assert all(similar_tracks.values())
        # We want this to fail when adding new svcs, for visibility
        assert len(similar_tracks.keys()) == (
            3 + (1 if track_type == match.SearchTrack else 0)
        )

    # Apple

    _assert_matches_all_services(AppleMusic, "deadmau5", "Strobe (Club Edit)")

    # Spotify

    _assert_matches_all_services(Spotify, "Avenged Sevenfold", "Almost Easy")

    # YouTube

    _assert_matches_all_services(
        YouTube, "Bon Iver", "Bon Iver - PDLIF - Official Video"
    )
    # Video actually separates title and artist
    _assert_matches_all_services(YouTube, "Bon Iver - Topic", "PDLIF")

    # YTMusic

    _assert_matches_all_services(
        YTMusic, "Jelly Roll", "Save Me (New Unreleased Video)"
    )

    # Search

    _assert_matches_all_services(
        None, None, "Jelly Roll - Save Me (New Unreleased Video)"
    )
