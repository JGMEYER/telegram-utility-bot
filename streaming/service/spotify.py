import base64
import json
import logging
import os
import requests
from urllib.parse import urljoin

from streaming import StreamingService, StreamingServiceTrack
from utils.log import setup_logger

setup_logger(__name__)
log = logging.getLogger(__name__)

BASE_API_URL = "https://api.spotify.com/v1/"
AUTHORIZE_URL = "https://accounts.spotify.com/api/token"

# # Enable HTTP debug logging for requests
# from http.client import HTTPConnection
# HTTPConnection.debuglevel = 1


class SpotifyToken:
    def __init__(self, token_type, access_token):
        self.token_type = token_type
        self.access_token = access_token

    def __str__(self):
        return f"{self.token_type} {self.access_token}"


def request_token():
    """Request Spotify access token"""
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

    client_credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(client_credentials.encode())

    headers = {
        "Authorization": f"Basic {encoded_credentials.decode()}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    try:
        response = requests.post(AUTHORIZE_URL, headers=headers, data=data)
        response.raise_for_status()
    except Exception:
        log.error("Requesting Spotify token", exc_info=True)
        return None

    content = json.loads(response.content)
    return SpotifyToken(content["token_type"], content["access_token"])


class SpotifyTrack(StreamingServiceTrack):
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
            else f"https://open.spotify.com/track/{self.id}"
        )


class Spotify(StreamingService):
    VALID_TRACK_URL_PATTERNS = [
        r"https://open.spotify.com/track/(?P<trackId>\w+)\??.*",
    ]

    def __enter__(self):
        self._token = request_token()
        return self

    def __exit__(self, *args):
        pass

    def get_track_from_trackId(self, trackId):
        track_url = urljoin(BASE_API_URL, f"tracks/{trackId}")
        headers = {"Authorization": str(self._token)}
        try:
            response = requests.get(track_url, headers=headers)
            response.raise_for_status()
        except Exception:
            log.error("Requesting Spotify track from id", exc_info=True)
            return None

        content = json.loads(response.content)
        if content:
            return SpotifyTrack(
                content["artists"][0]["name"], content["name"], trackId
            )
        else:
            return None

    def search_tracks(self, q, max_results=5):
        # Spotify sometimes doesn't deal well with dividers
        q = q.replace(" - ", " ")

        search_url = urljoin(BASE_API_URL, "search")
        headers = {
            "Authorization": str(self._token),
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        params = {"q": q, "type": "track", "limit": 1}
        try:
            search_response = requests.get(
                search_url, headers=headers, params=params
            )
            search_response.raise_for_status()
        except Exception:
            log.error("Searching Spotify track", exc_info=True)
            return None
        search_results = json.loads(search_response.content)

        tracks = []
        for res in search_results["tracks"]["items"]:
            track = SpotifyTrack(
                res["artists"][0]["name"],  # best guess
                res["name"],
                res["id"],
                res["external_urls"]["spotify"],
            )
            tracks.append(track)
        return tracks
