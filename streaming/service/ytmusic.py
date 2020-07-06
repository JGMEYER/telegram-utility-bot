import re

from ytmusicapi import YTMusic as YTMusicClient

from streaming import (
    StreamingService,
    StreamingServiceActionNotSupportedError,
    StreamingServiceTrack,
)


class YTMusicTrack(StreamingServiceTrack):
    """YTMusic song track

    Mirrors some of YouTubeTrack's logic. May make sense to later move these
    into a different base class later.
    """

    title = None
    artist = None
    id = None

    def __init__(self, title, artist, id):
        self.title = title
        self.artist = artist
        self.id = id

    def share_link(self):
        """WARNING: This is not going through an API and is subject to break"""
        return f"https://music.youtube.com/watch?v={self.id}"


class YTMusic(StreamingService):
    VALID_TRACK_URL_PATTERNS = [
        r"https://music.youtube.com/watch\?v=(?P<trackId>\w+).*",
    ]

    def __init__(self):
        self._client = None

    def __enter__(self):
        self._client = YTMusicClient()
        return self

    def __exit__(self, *args):
        pass

    def get_track_from_trackId(self, trackId):
        # We'll need to switch clients to support this feature
        raise StreamingServiceActionNotSupportedError()

    def search_tracks(self, q, max_results=None):
        del max_results  # unused, not available through client

        tracks = []
        for search_result in self._client.search(q, filter="songs"):
            track = search_result
            ytm_track = YTMusicTrack(
                track["title"], track["artists"][0]["name"], track["videoId"]
            )
            tracks.append(ytm_track)
        return tracks
