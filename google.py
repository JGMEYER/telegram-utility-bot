import os
from enum import Enum

import httplib2
from googleapiclient.discovery import build
from gmusicapi import Mobileclient

# Log all request/response headers and bodies
# httplib2.debuglevel = 4

class YoutubeContext():
    def __init__(self):
        self.client = None

    def __enter__(self):
        self.client = build('youtube', 'v3',
          developerKey=os.environ.get('YOUTUBE_API_KEY'))
        return self.client

    def __exit__(self, *args):
        pass


def search_youtube(yt, q, max_results=5):
    search_response = yt.search().list(
        q=q,
        part="id,snippet",
        maxResults=max_results,
    ).execute()

    videos = []
    for search_result in search_response.get("items", []):
        if search_result['id']['kind'] == "youtube#video":
            videos.append("%s (%s)" % (search_result['snippet']['title'],
                                       search_result['id']['videoId']))
    return videos


class GMusicContext():
    def __init__(self):
        self.client = Mobileclient()

    def __enter__(self):
        self.client.oauth_login(Mobileclient.FROM_MAC_ADDRESS)
        return self.client

    def __exit__(self, *args):
        self.client.logout()

class GMusicTrack():
    def __init__(self, name, artist, storeId):
        self.name = name
        self.artist = artist
        self.storeId = storeId

    def __str__(self):
        return f"'{self.name}' - {self.artist} ({self.storeId})"


def search_gmusic_tracks(gm, q, max_results=5):
    tracks = []
    for search_result in gm.search(q, max_results)['song_hits']:
        track = search_result['track']
        import pprint
        pprint.pprint(track)
        gm_track = GMusicTrack(track['title'], track['artist'], track['storeId'])
        tracks.append(gm_track)
    return tracks


if __name__ == "__main__":
    with YoutubeContext() as yt:
        import pprint
        pprint.pprint(search_youtube(yt, "G.o.a.t polyphia", max_results=5))
    with GMusicContext() as gm:
        import pprint
        tracks = search_gmusic_tracks(gm, "G.o.a.t polyphia", max_results=5)
        print(len(tracks))
        pprint.pprint([str(t) for t in tracks])
