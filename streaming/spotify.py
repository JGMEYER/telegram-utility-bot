import base64
import json
import logging
import os
import requests
from urllib.parse import urlencode, urljoin, urlparse
from http.client import HTTPConnection

BASE_API_URL = "https://api.spotify.com/v1/"
AUTHORIZE_URL = "https://accounts.spotify.com/api/token"

# enable HTTP debug logging for requests
# HTTPConnection.debuglevel = 1

def is_spotify_track_url(url):
    """Return if url matches Spotify track url"""
    return url.startswith('https://open.spotify.com/track/')

def track_id_from_track_url(url):
    """Retrieve track id from Spotify track url"""
    return urlparse(url).path.split('/track/')[1]


class SpotifyToken:
    def __init__(self, token_type, access_token):
        self.token_type = token_type
        self.access_token = access_token

    def __str__(self):
        return f"{self.token_type} {self.access_token}"

class SpotifyTrack:
    def __init__(self, name, artist):
        self.name = name
        self.artist = artist

    def __str__(self):
        return f"'{self.name}' - {self.artist}"


def request_token():
    """Request Spotify access token"""
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

    client_credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(client_credentials.encode())

    authorize_url = "https://accounts.spotify.com/api/token"
    headers = {'Authorization': f'Basic {encoded_credentials.decode()}'}
    data = {'grant_type': 'client_credentials'}
    try:
        response = requests.post(authorize_url, headers=headers, data=data)
        response.raise_for_status()
    except Exception as e:
        logging.error("Requesting Spotify token", exc_info=True)
        return None

    content = json.loads(response.content)
    return SpotifyToken(content['token_type'], content['access_token'])

def get_track_by_id(token, id):
    """GET spotify track by track id"""
    track_url = urljoin(BASE_API_URL, f"tracks/{id}")
    headers = {'Authorization': str(token)}
    try:
        response = requests.get(track_url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        logging.error("Requesting Spotify track", exc_info=True)
        return None

    content = json.loads(response.content)
    import pprint
    pprint.pprint(content)
    return SpotifyTrack(content['name'], content['artists'][0]['name'])


if __name__ == "__main__":
    """Integration Tests"""
    token = request_token()
    track_url = 'https://open.spotify.com/track/3h3pOvw6hjOvZxRUseB7h9?si=Ci-fm4N2TYq7kKlJANDnhA'
    track_id = track_id_from_track_url(track_url)
    print(get_track_by_id(token, track_id))
