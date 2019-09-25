import os
import re
from enum import Enum
from shutil import copyfile

from googleapiclient.discovery import build
from googleapiclient.discovery_cache.base import Cache
from gmusicapi import Mobileclient

from streaming import StreamingService, StreamingServiceTrack

# Log all request/response headers and bodies
# import httplib2
# httplib2.debuglevel = 4

class MemoryCache(Cache):
    """
    Workaround for "ModuleNotFoundError: No module named 'google.appengine'" when running on AWS.
    https://github.com/googleapis/google-api-python-client/issues/325#issuecomment-274349841
    """
    _CACHE = {}

    def get(self, url):
        return MemoryCache._CACHE.get(url)

    def set(self, url, content):
        MemoryCache._CACHE[url] = content


class YouTubeTrack(StreamingServiceTrack):
    name = None
    artist = None
    id = None

    def __init__(self, name, artist, id):
        self.name = name
        self.artist = artist
        self.id = id

    @property
    def searchable_name(self):
        # Remove mentioning of lyrics from the video title
        searchable_name = re.sub(r'\s(lyrics|with lyrics)$', '', self.name, flags=re.IGNORECASE)
        return searchable_name

    def share_link(self):
        """WARNING: This is not going through an API and is subject to break"""
        return f"https://www.youtube.com/watch?v={self.id}"

class YouTube(StreamingService):
    VALID_TRACK_URL_PATTERNS = [
        'https://www.youtube.com/watch\?v=(?P<trackId>[A-Za-z0-9\\-\\_]+).*',
        'https://(www.)?youtu.be/(?P<trackId>[A-Za-z0-9\\-\\_]+).*',
    ]

    def __init__(self):
        self._client = None

    def __enter__(self):
        self._client = build(
            'youtube',
            'v3',
            developerKey=os.getenv('YOUTUBE_API_KEY'),
            cache=MemoryCache())
        return self

    def __exit__(self, *args):
        pass

    def get_track_from_trackId(self, trackId):
        query_response = self._client.videos().list(
            id=trackId,
            part="id,snippet",
            maxResults=1,
        ).execute()
        if not query_response['items']:
            return None
        query_result = query_response['items'][0]
        track = YouTubeTrack(
            query_result['snippet']['title'],
            query_result['snippet']['channelTitle'],  # best guess
            query_result['id'],
        )
        return track

    def search_tracks(self, q, max_results=5):
        search_response = self._client.search().list(
            q=q,
            part="id,snippet",
            maxResults=max_results,
        ).execute()
        tracks = []
        for search_result in search_response.get("items", []):
            if search_result['id']['kind'] == "youtube#video":
                track = YouTubeTrack(
                    search_result['snippet']['title'],
                    search_result['snippet']['channelTitle'],  # best guess
                    search_result['id']['videoId'],
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
        "https://play.google.com/music/m/(?P<trackId>\w+)\\??.*",
    ]

    def __init__(self):
        self._client = Mobileclient()

    def __enter__(self):
        # AWS
        if os.getenv('LAMBDA_TASK_ROOT'):
            cred_path = os.path.join(os.environ['LAMBDA_TASK_ROOT'], "secrets", GMusic.CRED_FILE)
            # Only /tmp is writable on AWS lambda. gmusicapi needs to write to
            # the cred file to refresh its tokens.
            tmp_path = os.path.join("/tmp", GMusic.CRED_FILE)
            copyfile(cred_path, tmp_path)
            self._client.oauth_login(Mobileclient.FROM_MAC_ADDRESS, oauth_credentials=tmp_path)
        # Local
        else:
            cred_path = os.path.join(os.getcwd(), "secrets", GMusic.CRED_FILE)
            self._client.oauth_login(Mobileclient.FROM_MAC_ADDRESS, oauth_credentials=cred_path)
        return self

    def __exit__(self, *args):
        self._client.logout()

    def get_track_from_trackId(self, trackId):
        query_result = self._client.get_track_info(trackId)
        track = GMusicTrack(query_result['title'], query_result['artist'], query_result['storeId'])
        return track

    def search_tracks(self, q, max_results=5):
        tracks = []
        for search_result in self._client.search(q, max_results)['song_hits']:
            track = search_result['track']
            gm_track = GMusicTrack(track['title'], track['artist'], track['storeId'])
            tracks.append(gm_track)
        return tracks


if __name__ == "__main__":
    """Unit Tests"""
    assert YouTube.supports_track_url("https://www.youtube.com/watch?v=GWOIDN-akrY")  # supports dashes
    assert YouTube.supports_track_url("https://www.youtube.com/watch?v=9_gkpYORQLU")
    assert YouTube.supports_track_url("https://www.youtube.com/watch?v=9_gkpYORQLU?t=4")
    assert not YouTube.supports_track_url("https://www.youtube.com/")
    assert YouTube.supports_track_url("https://www.youtu.be/9_gkpYORQLU")
    assert YouTube.supports_track_url("https://www.youtu.be/9_gkpYORQLU?t=4")
    assert not YouTube.supports_track_url("https://www.youtu.be/")
    assert GMusic.supports_track_url("https://play.google.com/music/m/T2y24nzjhuyvlolsptj7zqon5qi")
    assert GMusic.supports_track_url("https://play.google.com/music/m/T2y24nzjhuyvlolsptj7zqon5qi?t=GOAT_-_Polyphia")
    assert not GMusic.supports_track_url("https://play.google.com/music/m/")

    assert YouTube.get_trackId_from_url("https://www.youtube.com/watch?v=GWOIDN-akrY"), "GWOIDN-akrY"  # supports dashes
    assert YouTube.get_trackId_from_url("https://www.youtube.com/watch?v=9_gkpYORQLU?t=4"), "9_gkpYORQLU"
    assert YouTube.get_trackId_from_url("https://www.youtu.be/9_gkpYORQLU?t=4"), "9_gkpYORQLU"
    assert GMusic.get_trackId_from_url("https://play.google.com/music/m/T2y24nzjhuyvlolsptj7zqon5qi?t=GOAT_-_Polyphia"), "T2y24nzjhuyvlolsptj7zqon5qi"

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
