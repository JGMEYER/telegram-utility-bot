import logging
import random
import re
from typing import Dict

from streaming import (
    SUPPORTED_STREAMING_SERVICES,
    StreamingServiceActionNotSupportedError,
    StreamingServiceTrack,
    YouTubeTrack,
    get_streaming_service_for_url,
)
from utils.log import setup_logger

setup_logger(__name__)
log = logging.getLogger(__name__)

# minimum ratio to consider streaming track titles a match
MINIMUM_ACCEPTED_TRACK_MATCH_RATIO = 0.80  # arbitrary


def urls_in_text(text):
    """Retrieves list of valid urls from text"""
    urls = [w for w in text.split() if re.match("http[s]?://.*", w)]
    return urls


class SearchTrack(YouTubeTrack):
    """
    HACK: At time of writing, YouTubeTrack is the only type that can more intelligently parse out the artist
    and track from a single title. We abuse that fact here to avoid rewriting logic.
    """

    def __init__(self, title, *argv):
        super().__init__(title, None, None)

    def share_link(self):
        raise NotImplementedError(
            "A search track does not have an associated URL"
        )


def search_track_in_text(text):
    # TODO grab bot name from env var
    match = re.search(r"\@BopizTestBot\s(?P<title>.*)", text)
    if match is None:
        return None

    title = match.group("title")
    return SearchTrack(title)


SEARCH_NOT_FOUND_MESSAGES = [
    "Me, an empath, sensing that that song doesn't exist.",
    "Song not found. Did you try switching it to Wumbo?",
    "That's not a real song, don't gaslight me.",
    "Look, I tried my best okay? The song's not there.",
    "There's approximately 97 million songs in the world. That was not one of them.",
    "Ah sorry, seems that song is out of stock. Supply chain issues, y'know?",
    "Sometimes I find the song you're looking for... this is not one of those times.",
]


def get_search_result_message(searchable_name, similar_tracks, search_author):
    log.info(f"similar_tracks: {similar_tracks}")

    if not any(similar_tracks.values()):
        fail_msg = random.choice(SEARCH_NOT_FOUND_MESSAGES)
        return f"@{search_author} {fail_msg}"

    # Generates message like:
    #   """
    #   Title - Artist
    #   Spotify | YouTube | YTMusic
    #   """
    msg = ""
    msg += f"{searchable_name}:\n"
    msg += " | ".join(
        [
            f"[{svc_name}]({t.share_link()})" if t else f"{svc_name}"
            for svc_name, t in sorted(similar_tracks.items())
        ]
    )

    return msg


def get_mirror_links_message(urls):
    """Generate message to display mirror link results"""
    similar_tracks = get_similar_tracks_from_urls(urls, include_original=True)
    log.info(f"similar_tracks: {similar_tracks}")

    if not similar_tracks:
        log.info("No mirrors found for tracks")
        return None

    msg = ""
    for track, track_matches in similar_tracks.items():
        # Need more than just the original link to display mirrors
        if len([m for m in track_matches.values() if m is not None]) < 2:
            log.info(
                f"No mirrors to send for track (share_link: "
                f"{track.share_link()})"
            )
        else:
            # Generates message like:
            #   """
            #   Song - Artist
            #   Spotify | YouTube | YTMusic
            #
            #   Song - Artist
            #   Spotify | YouTube | YTMusic
            #   """
            if msg:
                msg += "\n\n"
            msg += f"{track.searchable_name}:\n"
            msg += " | ".join(
                [
                    f"[{svc_name}]({t.share_link()})" if t else f"{svc_name}"
                    for svc_name, t in sorted(track_matches.items())
                ]
            )

    return msg if msg else None


def get_similar_tracks_from_urls(urls, include_original=False):
    """Attempts to retrieve mirror links to all other streaming services for
    track provided in URL
    """
    # Format: {original_track: {svc: track, ..}, ..}
    similar_tracks: Dict[
        StreamingServiceTrack, Dict[str, StreamingServiceTrack]
    ] = {}
    log.info(f"urls: {urls}")
    for url in urls:
        log.info(f"URL detected (url: {url})")
        svc = get_streaming_service_for_url(url)
        if svc:
            trackId = svc.get_trackId_from_url(url)
            log.info(f"url: {url} ; trackId: {trackId}")

            try:
                with svc() as svc_client:
                    original_track = svc_client.get_track_from_trackId(trackId)
            except StreamingServiceActionNotSupportedError:
                log.info(
                    "Client does not support get_track_from_trackId",
                    exc_info=True,
                )
                continue
            except Exception:
                log.error("Getting track from track id", exc_info=True)
                continue

            similar_tracks_from_original = get_similar_tracks_for_original_track(  # noqa: E501
                svc, original_track
            )
            if include_original:
                similar_tracks_from_original[svc.__name__] = original_track

            similar_tracks[original_track] = similar_tracks_from_original
        else:
            log.info(
                f"URL is not for a supported streaming service (url: "
                f"{url})"
            )
            continue
    return similar_tracks


def get_similar_tracks_for_original_track(track_svc, original_track):
    """Returns dict of urls from other streaming services for the same track"""
    similar_tracks: Dict[str, StreamingServiceTrack] = {}
    for svc in SUPPORTED_STREAMING_SERVICES:
        if svc is track_svc:
            continue

        track = None
        with svc() as svc_client:
            try:
                track = svc_client.search_one_track(
                    original_track.searchable_name
                )
            except Exception:
                log.error("Searching one track", exc_info=True)

        if track:
            if tracks_are_similar(original_track, track):
                similar_tracks[svc.__name__] = track
            else:
                similar_tracks[svc.__name__] = None
                log.warning(
                    f'Track title "{track.searchable_name}" for '
                    f"svc {svc.__name__} is not similar enough to "
                    f'"{original_track.searchable_name}".'
                )
        else:
            similar_tracks[svc.__name__] = None

    return similar_tracks


def tracks_are_similar(track_a, track_b):
    """Returns whether two tracks meet the mimimum similarity ratio.

    We test the ratio both ways since each StreamingServiceTrack class can have
    its own logic for checking similarity
    """
    sim_ratio_ab = track_a.similarity_ratio(track_b)
    sim_ratio_ba = track_b.similarity_ratio(track_a)
    sim_ratio = max(sim_ratio_ab, sim_ratio_ba)
    log.info(f"Similarity checks: {sim_ratio_ab}, {sim_ratio_ba}")
    return sim_ratio >= MINIMUM_ACCEPTED_TRACK_MATCH_RATIO
