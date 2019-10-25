import os
import sys

# add project modules to path so we can import them
proj_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..")
sys.path.append(proj_path)

import handler
from streaming import SUPPORTED_STREAMING_SERVICES
from streaming.google import YouTube, YouTubeVideoCategory


def test_youtube_matches():
    """
    Tests how effectively we match YouTube tracks against their results.

    YouTube names are unstandardized so it's difficult to ensure that we can
    properly search other services and get correct results. This test pulls
    an arbitrary set of YouTube videos to test the logic we've created
    elsewhere to find matches for these videos on other services.
    """
    with YouTube() as yt:
        tracks = yt.search_tracks("", max_results=5, video_category_id=
                                  YouTubeVideoCategory.MUSIC.value)

    track_matches = {}
    for track in tracks:
        similar_tracks = handler.get_similar_tracks_for_original_track(YouTube,
                                                                       track)
        track_matches[track.searchable_name] = similar_tracks

    missing_msgs = []
    for track_src_name, matches in track_matches.items():
        for svc in SUPPORTED_STREAMING_SERVICES:
            if svc is YouTube:
                continue
            if svc.__name__ not in matches.keys():
                missing_msgs.append(f"\"{track_src_name}\" is missing result "
                                    f"for {svc.__name__}")

    if missing_msgs:
        print('\n'.join(missing_msgs))
        sys.exit(1)


if __name__ == "__main__":
    test_youtube_matches()
