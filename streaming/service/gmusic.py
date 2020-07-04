import os
from shutil import copyfile

from gmusicapi import Mobileclient

from streaming import StreamingService, StreamingServiceTrack


class GMusicTrack(StreamingServiceTrack):
    """GMusic song track"""

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
    """GMusic client"""

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
