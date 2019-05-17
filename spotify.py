import base64
import json
import logging
import os
import requests
from http.client import HTTPConnection

BASE_API_URL = "https://api.spotify.com/v1/"
AUTHORIZE_URL = "https://accounts.spotify.com/api/token"

# enable HTTP debug logging for requests
HTTPConnection.debuglevel = 1

"""
TODO
Test on getting track
"""

class SpotifyToken:
    def __init__(self, access_token, token_type):
        self.access_token = access_token
        self.token_type = token_type

def request_token():
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

    client_credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(client_credentials.encode())

    authorize_url = "https://accounts.spotify.com/api/token"
    headers = {'Authorization': f'Basic {encoded_credentials.decode()}'} #{encoded_credentials}'}
    data = {'grant_type': 'client_credentials'}
    try:
        response = requests.post(authorize_url, headers=headers, data=data)
        response.raise_for_status()
    except Exception as e:
        logging.error("Requesting Spotify token", exc_info=True)
        return None

    content = json.loads(response.content)
    return SpotifyToken(content['access_token'], content['token_type'])

def get_track_by_id(access_token, id):
    return None  # unimplemented

if __name__ == "__main__":
    token = request_token()
    print(get_track_by_id(token, "3h3pOvw6hjOvZxRUseB7h9"))
