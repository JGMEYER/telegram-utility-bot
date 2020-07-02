# Ideally, this wouldn't be exported with the module
from .streaming import StreamingService, StreamingServiceTrack  # noqa: F401

from .google_ import YouTube, YouTubeTrack  # noqa: F401
from .google_ import GMusic, GMusicTrack  # noqa: F401
from .spotify import Spotify, SpotifyTrack  # noqa: F401

SUPPORTED_STREAMING_SERVICES = StreamingService.__subclasses__()


def get_streaming_service_for_url(url):
    for svc in SUPPORTED_STREAMING_SERVICES:
        if svc.supports_track_url(url):
            return svc
    return None
