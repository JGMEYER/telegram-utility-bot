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
    artist = None
    title = None
    id = None

    def __init__(self, artist, title, trackId, url=None):
        self.artist = artist
        self.title = title
        self.id = trackId
        self.url = url

    def share_link(self):
        """WARNING: This is not going through an API and is subject to break"""
        return (
            self.url
            if self.url
            # TODO test this
            else f"what to return? do I need all the album info?"
        )


class AppleMusic(StreamingService):
    VALID_TRACK_URL_PATTERNS = [
        r"https://music.apple.com/(?P<appleStorefront>\w+)/album/(?P<appleTrackName>[\w\-]+)/(?P<albumId>\d+)\?i=(?P<trackId>\d+)",  # noqa: E501
    ]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def get_track_from_trackId(self, trackId):
        pass

    def search_tracks(self, q, max_results=5):
        # Apple Music requires '+' delimiter instead of spaces
        q = q.replace(" ", "+")

        token = getenv("APPLE_DEVELOPER_JWT")

        search_url = urljoin(BASE_API_URL, f"catalog/{STOREFRONT}/search")
        # TODO headers
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "types": "songs",
            "with": "topResults",
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
        for res in search_results["results"]["songs"]["data"]:
            track = AppleMusicTrack(
                res["attributes"]["artistName"],
                res["attributes"]["name"],
                res["attributes"]["playParams"]["id"],
                res["attributes"]["url"],
            )
            tracks.append(track)
        return tracks
