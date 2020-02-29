import html
import os
import re
from difflib import SequenceMatcher
from enum import IntEnum
from shutil import copyfile

from googleapiclient.discovery import build
from googleapiclient.discovery_cache.base import Cache
from gmusicapi import Mobileclient

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
        searchable_name = html.unescape(self.name)
        # Remove terms that negatively impact our search on other platforms
        for exp in self.SEARCHABLE_EXCLUDE_EXPRESSIONS:
            searchable_name = re.sub(
                exp, "", searchable_name, flags=re.IGNORECASE
            )
        return searchable_name.strip()

    def share_link(self):
        """WARNING: This is not going through an API and is subject to break"""
        return f"https://www.youtube.com/watch?v={self.id}"

    def similarity_ratio(self, other_track):
        """Overrides StreamingServiceTrack.similarity_ratio()

        YouTube titles don't adhere to any convention and may occasionally swap
        the artist and track title. This method tries rearranging the video
        title to better check for a match with another track.
        """

        ratio = SequenceMatcher(
            None, self.searchable_name, other_track.searchable_name
        ).ratio()

        # symbols that may lie between an artist and track title
        title_dividers = {"-", "|"}

        for div in title_dividers:
            splits = [
                idx
                for idx, chr in enumerate(self.searchable_name)
                if chr == div
            ]
            for idx in splits:
                left = self.searchable_name[:idx].strip()
                right = self.searchable_name[idx + 1 :].strip()
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
        print([q, "id,snippet", "video", max_results, video_category_id])
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


class GMusicTrack(StreamingServiceTrack):
    name = None
    artist = None
    id = None

    def __init__(self, name, artist, storeId):
        self.name = name
        self.artist = artist
        self.id = storeId

    def share_link(self):
        """WARNING: This is not going through an API and is subject to break"""
        return f"https://play.google.com/music/m/{self.id}"


class GMusic(StreamingService):
    CRED_FILE = "gmusicapi.cred"
    VALID_TRACK_URL_PATTERNS = [
        r"https://play.google.com/music/m/(?P<trackId>\w+)\??.*",
    ]

    def __init__(self):
        self._client = Mobileclient()

    def __enter__(self):
        # AWS / Docker
        if (
            os.getenv("LAMBDA_TASK_ROOT")
            and os.environ["SERVERLESS_STAGE"] != "local"
        ):
            cred_path = os.path.join(
                os.environ["LAMBDA_TASK_ROOT"], "secrets", GMusic.CRED_FILE
            )
            # Only /tmp is writable on AWS lambda. gmusicapi needs to write to
            # the cred file to refresh its tokens.
            tmp_path = os.path.join("/tmp", GMusic.CRED_FILE)
            copyfile(cred_path, tmp_path)
            self._client.oauth_login(
                Mobileclient.FROM_MAC_ADDRESS, oauth_credentials=tmp_path
            )
        # Local
        else:
            cred_path = os.path.join(os.getcwd(), "secrets", GMusic.CRED_FILE)
            self._client.oauth_login(
                Mobileclient.FROM_MAC_ADDRESS, oauth_credentials=cred_path
            )
        return self

    def __exit__(self, *args):
        self._client.logout()

    def get_track_from_trackId(self, trackId):
        query_result = self._client.get_track_info(trackId)
        track = GMusicTrack(
            query_result["title"],
            query_result["artist"],
            query_result["storeId"],
        )
        return track

    def search_tracks(self, q, max_results=5):
        tracks = []
        for search_result in self._client.search(q, max_results)["song_hits"]:
            track = search_result["track"]
            gm_track = GMusicTrack(
                track["title"], track["artist"], track["storeId"]
            )
            tracks.append(gm_track)
        return tracks


if __name__ == "__main__":
    """Unit Tests"""
    assert YouTube.supports_track_url(
        "https://www.youtube.com/watch?v=GWOIDN-akrY"
    )
    assert YouTube.supports_track_url(
        "https://www.youtube.com/watch?v=9_gkpYORQLU"
    )
    assert YouTube.supports_track_url(
        "https://www.youtube.com/watch?v=9_gkpYORQLU?t=4"
    )
    assert not YouTube.supports_track_url("https://www.youtube.com/")
    assert YouTube.supports_track_url("https://www.youtu.be/9_gkpYORQLU")
    assert YouTube.supports_track_url("https://www.youtu.be/9_gkpYORQLU?t=4")
    assert not YouTube.supports_track_url("https://www.youtu.be/")
    assert GMusic.supports_track_url(
        "https://play.google.com/music/m/T2y24nzjhuyvlolsptj7zqon5qi"
    )
    assert GMusic.supports_track_url(
        "https://play.google.com/music/m/T2y24nzjhuyvlolsptj7zqon5qi?t=GOAT_-_Polyphia"  # noqa: E501
    )
    assert not GMusic.supports_track_url("https://play.google.com/music/m/")

    assert YouTube.get_trackId_from_url(
        "https://www.youtube.com/watch?v=GWOIDN-akrY"
    ), "GWOIDN-akrY"
    assert YouTube.get_trackId_from_url(
        "https://www.youtube.com/watch?v=9_gkpYORQLU?t=4"
    ), "9_gkpYORQLU"
    assert YouTube.get_trackId_from_url(
        "https://www.youtu.be/9_gkpYORQLU?t=4"
    ), "9_gkpYORQLU"
    assert GMusic.get_trackId_from_url(
        "https://play.google.com/music/m/T2y24nzjhuyvlolsptj7zqon5qi?t=GOAT_-_Polyphia"  # noqa: E501
    ), "T2y24nzjhuyvlolsptj7zqon5qi"

    """Integration Tests"""
    with YouTube() as yt:
        track = yt.search_one_track("G.o.a.t polyphia")
        print(track)
        trackId = YouTube.get_trackId_from_url(track.share_link())
        print(trackId)
        track = yt.get_track_from_trackId(trackId)
        print(track)
        print(track.share_link())
    print()
    with GMusic() as gm:
        track = gm.search_one_track("G.o.a.t polyphia")
        print(track)
        trackId = GMusic.get_trackId_from_url(track.share_link())
        print(trackId)
        track = gm.get_track_from_trackId(trackId)
        print(track)
        print(track.share_link())
