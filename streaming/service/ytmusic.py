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

    # Regexp to exclude from searchable video names
    SEARCHABLE_EXCLUDE_EXPRESSIONS = [
        r"\s\(?(HD\s?)?((with |w\/ )?lyrics)?\)?$",  # ()'s
        r"\s\[?(HD\s?)?((with |w\/ )?lyrics)?\]?$",  # []'s
        r"\((Official\s)?(Music\s|Lyric\s)?(Video|Movie|Audio)\)",  # ()'s
        r"\[(Official\s)?(Music\s|Lyric\s)?(Video|Movie|Audio)\]",  # []'s
    ]

    name = None
    artist = None
    id = None

    def __init__(self, name, artist, id):
        self.name = name
        self.artist = artist
        self.id = id

    @property
    def searchable_name(self):
        """NOTE: This override may not be necessary, based on YTMusic's
        titling. Worth testing and removing, if so."""
        searchable_track_name = self.name
        # Remove terms that negatively impact our search on other platforms
        for exp in self.SEARCHABLE_EXCLUDE_EXPRESSIONS:
            searchable_track_name = re.sub(
                exp, "", searchable_track_name, flags=re.IGNORECASE
            )
        return f"{searchable_track_name.strip()} - {self.artist}"

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
