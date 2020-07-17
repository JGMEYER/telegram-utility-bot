import os
from difflib import SequenceMatcher
from enum import IntEnum

from googleapiclient.discovery import build
from googleapiclient.discovery_cache.base import Cache

from streaming import StreamingService, StreamingServiceTrack

# Log all request/response headers and bodies
# import httplib2
# httplib2.debuglevel = 4


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


class YouTubeTrack(StreamingServiceTrack):
    """YouTube song track"""

    # Symbols that may lie between an artist and track title
    SEARCHABLE_NAME_DIVIDERS = {"-", "|", "»"}

    title = None
    artist = None
    id = None

    def __init__(self, title, artist, id):
        self.title = title
        self.artist = (
            artist  # YouTube does not always provide artist information
        )
        self.id = id

    @property
    def searchable_name(self):
        """Overrides StreamingServiceTrack.searchable_name()"""

        # If the artist is already in the video name, ignore
        if self.cleaned_artist.lower() in self.cleaned_title.lower():
            return self.cleaned_title.lower()

        return f"{self.cleaned_title} - {self.cleaned_artist}".lower()

    def share_link(self):
        """WARNING: This is not going through an API and is subject to break"""
        return f"https://www.youtube.com/watch?v={self.id}"

    def similarity_ratio(self, other_track):
        """Overrides StreamingServiceTrack.similarity_ratio()

        YouTube titles don't adhere to any convention. Try a few approaches to
        better check for a match with another track.
        """

        ratio = super().similarity_ratio(other_track)

        # Rearrange video title in case track title and artist are swapped
        for div in self.SEARCHABLE_NAME_DIVIDERS:
            splits = [
                idx
                for idx, chr in enumerate(self.searchable_name)
                if chr == div
            ]
            for idx in splits:
                left = self.searchable_name[:idx].strip()
                right = self.searchable_name[idx + 1 :].strip()  # noqa: E203
                # use '-' as the new divider since its the most standard
                swapped_name = f"{right} - {left}"
                new_ratio = SequenceMatcher(
                    None, swapped_name, other_track.searchable_name
                ).ratio()
                ratio = max(ratio, new_ratio)

        return ratio


class YouTubeVideoCategory(IntEnum):
    MUSIC = 10  # available in regionCode: US


class YouTube(StreamingService):
    """YouTube client"""

    VALID_TRACK_URL_PATTERNS = [
        r"https://www.youtube.com/watch\?v=(?P<trackId>[A-Za-z0-9\-\_]+).*",
        r"https://(www.)?youtu.be/(?P<trackId>[A-Za-z0-9\-\_]+).*",
    ]

    def __init__(self):
        self._client = None

    def __enter__(self):
        self._client = build(
            "youtube",
            "v3",
            developerKey=os.getenv("YOUTUBE_API_KEY"),
            cache=MemoryCache(),
        )
        return self

    def __exit__(self, *args):
        pass

    def get_track_from_trackId(self, trackId):
        query_response = (
            self._client.videos()
            .list(id=trackId, part="id,snippet", maxResults=1,)
            .execute()
        )
        if not query_response["items"]:
            return None
        query_result = query_response["items"][0]
        track = YouTubeTrack(
            query_result["snippet"]["title"],
            query_result["snippet"]["channelTitle"],  # best guess
            query_result["id"],
        )
        return track

    def search_tracks(self, q, max_results=5, video_category_id=None):
        search_response = (
            self._client.search()
            .list(
                q=q,
                part="id,snippet",
                type="video",
                maxResults=max_results,
                videoCategoryId=video_category_id,
            )
            .execute()
        )
        tracks = []
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                track = YouTubeTrack(
                    search_result["snippet"]["title"],
                    search_result["snippet"]["channelTitle"],  # best guess
                    search_result["id"]["videoId"],
                )
                tracks.append(track)
        return tracks
