import json
import logging
import requests
from urllib.parse import urljoin

from streaming import StreamingService, StreamingServiceTrack
from utils.env import getenv
from utils.log import setup_logger

setup_logger(__name__)
log = logging.getLogger(__name__)

STOREFRONT = "us"
BASE_API_URL = "https://api.music.apple.com/v1/"


class AppleMusicTrack(StreamingServiceTrack):
    # Override abstract properties
    artist = None
    title = None
    id = None

    def __init__(self, artist, title, trackId, url=None):
        self.artist = artist
        self.title = title
        self.id = trackId
        self.url = url

    def share_link(self):
        if not self.url:
            # This should never be left unset outside a test case
            raise AttributeError("self.url never defined")
        return self.url


class AppleMusic(StreamingService):
    VALID_TRACK_URL_PATTERNS = [
        r"https://music.apple.com/(?P<appleStorefront>\w+)/album/(?P<appleTrackName>[\w\-]+)/(?P<albumId>\d+)\?i=(?P<trackId>\d+)",  # noqa: E501
    ]

    def __enter__(self):
        self._token = getenv("APPLE_DEVELOPER_JWT").replace('"', "")
        return self

    def __exit__(self, *args):
        pass

    def get_track_from_trackId(self, trackId):
        songs_url = urljoin(BASE_API_URL, f"catalog/{STOREFRONT}/songs")
        headers = {"Authorization": f"Bearer {self._token}"}
        params = {"ids": str(trackId)}
        try:
            songs_response = requests.get(
                songs_url, headers=headers, params=params
            )
            songs_response.raise_for_status()
        except Exception as e:
            log.error("Requesting Apple Music track from id", exc_info=True)
            raise e

        songs_results = json.loads(songs_response.content)
        if songs_results["data"]:
            res = songs_results["data"][0]
            return AppleMusicTrack(
                res["attributes"]["artistName"],
                res["attributes"]["name"],
                res["attributes"]["playParams"]["id"],
                res["attributes"]["url"],
            )
        else:
            return None

    def search_tracks(self, q, max_results=5):
        search_url = urljoin(BASE_API_URL, f"catalog/{STOREFRONT}/search")
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self._token}",
        }
        params = {
            "types": "songs",
            "with": "topResults",
            "term": q,  # requests lib should convert all spaces to "+"
        }
        try:
            search_response = requests.get(
                search_url, headers=headers, params=params
            )
            search_response.raise_for_status()
        except Exception:
            log.error("Searching Apple Music track", exc_info=True)
            return None
        search_results = json.loads(search_response.content)

        tracks = []
        if search_results["results"]:
            for res in search_results["results"]["songs"]["data"]:
                track = AppleMusicTrack(
                    res["attributes"]["artistName"],
                    res["attributes"]["name"],
                    res["attributes"]["playParams"]["id"],
                    res["attributes"]["url"],
                )
                tracks.append(track)
        return tracks
