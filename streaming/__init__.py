# Ideally, this wouldn't be exported with the module
from .streaming import StreamingService, StreamingServiceTrack

from .google import YouTube, YouTubeTrack
from .google import GMusic, GMusicTrack
from .spotify import Spotify, SpotifyTrack

SUPPORTED_STREAMING_SERVICES = StreamingService.__subclasses__()

def get_streaming_service_for_url(url):
    for svc in SUPPORTED_STREAMING_SERVICES:
        if svc.supports_track_url(url):
            return svc
    return None
