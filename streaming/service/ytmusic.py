import os

from googleapiclient.discovery import build
from googleapiclient.discovery_cache.base import Cache

from ytmusicapi import YTMusic as YTMusicClient
from streaming import (
    StreamingService,
    StreamingServiceTrack,
)


class MemoryCache(Cache):
    """Workaround for "ModuleNotFoundError: No module named 'google.appengine'"
    when running on AWS.
    https://github.com/googleapis/google-api-python-client/issues/325#issuecomment-274349841
    """

    _CACHE = {}

    def get(self, url):
        return MemoryCache._CACHE.get(url)

    def set(self, url, content):
        MemoryCache._CACHE[url] = content


class YTMusicTrack(StreamingServiceTrack):
    """YTMusic song track

    Mirrors some of YouTubeTrack's logic. May make sense to later move these
    into a different base class later.
    """

    # Override abstract properties
    artist = None
    title = None
    id = None

    def __init__(self, artist, title, id):
        self.artist = artist
        self.title = title
        self.id = id

    def share_link(self):
        """WARNING: This is not going through an API and is subject to break"""
        return f"https://music.youtube.com/watch?v={self.id}"


class YTMusic(StreamingService):
    VALID_TRACK_URL_PATTERNS = [
        r"https://music.youtube.com/watch\?v=(?P<trackId>[a-zA-z0-9\-\_]+).*",
    ]

    def __init__(self):
        self._yt_client = None
        self._ytmusic_client = None

    def __enter__(self):
        self._yt_client = build(
            "youtube",
            "v3",
            developerKey=os.getenv("YOUTUBE_API_KEY"),
            cache=MemoryCache(),
        )
        self._ytmusic_client = YTMusicClient()
        return self

    def __exit__(self, *args):
        pass

    def get_track_from_trackId(self, trackId):
        """Use YouTube's API to extract information for the YTMusic video.

        A lot of research went into this. This seems to be the easiest route
        forwards. See: https://github.com/sigma67/ytmusicapi/issues/42"""
        query_response = (
            self._yt_client.videos()
            .list(
                id=trackId,
                part="id,snippet",
                maxResults=1,
            )
            .execute()
        )
        if not query_response["items"]:
            return None
        query_result = query_response["items"][0]
        track = YTMusicTrack(
            query_result["snippet"]["channelTitle"],  # best guess
            query_result["snippet"]["title"],
            query_result["id"],
        )
        return track

    def search_tracks(self, q, max_results=None):
        del max_results  # unused, not available through client

        tracks = []
        for search_result in self._ytmusic_client.search(q, filter="songs"):
            track = search_result

            # sometimes no artist set
            artist = track["artists"][0]["name"] if track["artists"] else None

            ytm_track = YTMusicTrack(artist, track["title"], track["videoId"])
            tracks.append(ytm_track)

        return tracks
