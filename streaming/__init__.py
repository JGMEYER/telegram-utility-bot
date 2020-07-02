# Ideally, this wouldn't be exported with the module
from .streaming import (  # noqa: F401
    StreamingService,
    StreamingServiceActionNotSupportedError,
    StreamingServiceTrack,
)

from .service_gmusic import GMusic, GMusicTrack  # noqa: F401
from .service_youtube import YouTube, YouTubeTrack  # noqa: F401
from .service_ytmusic import YTMusic, YTMusicTrack  # noqa: F401
from .service_spotify import Spotify, SpotifyTrack  # noqa: F401

SUPPORTED_STREAMING_SERVICES = StreamingService.__subclasses__()


def get_streaming_service_for_url(url):
    for svc in SUPPORTED_STREAMING_SERVICES:
        if svc.supports_track_url(url):
            return svc
    return None
