import os
from enum import Enum

import httplib2
from googleapiclient.discovery import build
from gmusicapi import Mobileclient

from streaming import StreamingService, StreamingServiceTrack

# Log all request/response headers and bodies
# httplib2.debuglevel = 4

class YouTubeTrack(StreamingServiceTrack):
    name = None
    artist = None
    id = None

    def __init__(self, name, artist, id):
        self.name = name
        self.artist = artist
        self.id = id

    def share_link(self):
        """WARNING: This is not going through an API and is subject to break"""
        return f"https://www.youtube.com/watch?v={self.id}"

class YouTube(StreamingService):
    def __init__(self):
        self._client = None

    def __enter__(self):
        self._client = build('youtube', 'v3',
          developerKey=os.environ.get('YOUTUBE_API_KEY'))
        return self

    def __exit__(self, *args):
        pass

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

    def supports_url(url):
        pass

    def get_track_name_from_url(url):
        pass


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
    def __init__(self):
        self._client = Mobileclient()

    def __enter__(self):
        self._client.oauth_login(Mobileclient.FROM_MAC_ADDRESS)
        return self

    def __exit__(self, *args):
        self._client.logout()

    def search_tracks(self, q, max_results=5):
        tracks = []
        for search_result in self._client.search(q, max_results)['song_hits']:
            track = search_result['track']
            gm_track = GMusicTrack(track['title'], track['artist'], track['storeId'])
            tracks.append(gm_track)
        return tracks

    def supports_url(url):
        pass

    def get_track_name_from_url(url):
        pass


if __name__ == "__main__":
    """Integration Tests"""
    with GMusic() as gm:
        track = gm.search_one_track("G.o.a.t polyphia")
        print(track)
        print(track.share_link())
    with YouTube() as yt:
        track = yt.search_one_track("G.o.a.t polyphia")
        print(track)
        print(track.share_link())
