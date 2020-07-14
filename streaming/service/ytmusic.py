# TODO rm
# import re
# import requests
# import urllib.parse
# from bs4 import BeautifulSoup
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


# TODO this may all be replaceable by following the first step of
# https://www.youtube.com/get_video_info?video_id=e_S9VvJM1PI
# i.e. just call https://www.youtube.com/get_video_info?video_id={videoId}

# class STSFinder:
#     """To call the YouTube's reverse-engineered get_video_info/ endpoint, we
#     need an `sts` value. This class is dedicated to fetching this value.
#     """

#     # TODO rm
#     # EMBED_PLAYER_JS_PATTERN = (
#     #     r"/yts/jsbin/www-embed-player-(?P<trackId>\w+)/www-embed-player.js"
#     # )

#     @classmethod
#     def get_sts(cls, trackId):
#         embed_html = cls._get_video_embed_page_html(trackId)
#         base_js_url = cls._get_base_js_url(embed_html)
#         sts = cls._extract_sts_from_base_js(base_js_url)

#         return sts  # TODO

#     @classmethod
#     def _get_video_embed_page_html(cls, trackId):
#         page = requests.get(f"https://www.youtube.com/embed/{trackId}")
#         return page.text

#     @classmethod
#     def _get_base_js_url(cls, embed_html):
#         soup = BeautifulSoup(embed_html, "html.parser")
#         script_tag = soup.find(
#             "script", {"name": "www-embed-player/www-embed-player"}
#         )
#         embed_player_path = script_tag["src"]

#         # Extract playerid from player path
#         match = re.search(
#             r"/yts/jsbin/www-embed-player-(?P<player_id>\w+)/www-embed-player.js",
#             embed_player_path,
#         )
#         if not match:
#             raise Exception(
#                 "Could not extract player_id from embed_player_path"
#             )
#         player_id = match.group("player_id")

#         return f"https://www.youtube.com/yts/jsbin/player-{player_id}/en_US/base.js"

#     @classmethod
#     def _extract_sts_from_base_js(cls, base_js_url):
#         print(base_js_url)
#         page = requests.get(base_js_url)
#         match = re.search(r"\,sts\:(?P<sts>\d+)", page.text)
#         # print(page.text)
#         print(match)
#         return match


class YTMusic(StreamingService):
    VALID_TRACK_URL_PATTERNS = [
        r"https://music.youtube.com/watch\?v=(?P<trackId>\w+).*",
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
            .list(id=trackId, part="id,snippet", maxResults=1,)
            .execute()
        )
        if not query_response["items"]:
            return None
        query_result = query_response["items"][0]
        track = YTMusicTrack(
            query_result["snippet"]["title"],
            query_result["snippet"]["channelTitle"],  # best guess
            query_result["id"],
        )
        return track

    def search_tracks(self, q, max_results=None):
        del max_results  # unused, not available through client

        tracks = []
        for search_result in self._ytmusic_client.search(q, filter="songs"):
            track = search_result
            ytm_track = YTMusicTrack(
                track["title"], track["artists"][0]["name"], track["videoId"]
            )
            tracks.append(ytm_track)
        return tracks
