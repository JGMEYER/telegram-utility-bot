import html
import re
from difflib import SequenceMatcher

from ytmusicapi import YTMusic as YTMusicClient

from streaming import (
    StreamingService,
    StreamingServiceActionNotSupportedError,
    StreamingServiceTrack,
)


class YTMusicTrack(StreamingServiceTrack):
    """YTMusic song track

    Mirrors much of YouTubeTrack's logic. May make sense to later move these
    into a different base class later.
    """

    # Regexp to exclude from searchable video names
    SEARCHABLE_EXCLUDE_EXPRESSIONS = [
        r"\s\(?(HD\s?)?((with |w\/ )?lyrics)?\)?$",  # ()'s
        r"\s\[?(HD\s?)?((with |w\/ )?lyrics)?\]?$",  # []'s
        r"\((Official\s)?(Music\s|Lyric\s)?(Video|Movie|Audio)\)",  # ()'s
        r"\[(Official\s)?(Music\s|Lyric\s)?(Video|Movie|Audio)\]",  # []'s
    ]

    name = None
    artist = None
    id = None

    def __init__(self, name, artist, storeId):
        self.name = name
        self.artist = artist
        self.id = storeId

    @property
    def searchable_name(self):
        searchable_name = html.unescape(self.name)
        # Remove terms that negatively impact our search on other platforms
        for exp in self.SEARCHABLE_EXCLUDE_EXPRESSIONS:
            searchable_name = re.sub(
                exp, "", searchable_name, flags=re.IGNORECASE
            )
        return searchable_name.strip()

    def share_link(self):
        """WARNING: This is not going through an API and is subject to break"""
        return f"https://music.youtube.com/watch?v={self.id}"

    def similarity_ratio(self, other_track):
        """Overrides StreamingServiceTrack.similarity_ratio()

        YTMusic titles don't adhere to any convention and may occasionally swap
        the artist and track title. This method tries rearranging the video
        title to better check for a match with another track.
        """

        ratio = SequenceMatcher(
            None, self.searchable_name, other_track.searchable_name
        ).ratio()

        # symbols that may lie between an artist and track title
        title_dividers = {"-", "|"}

        for div in title_dividers:
            splits = [
                idx
                for idx, chr in enumerate(self.searchable_name)
                if chr == div
            ]
            for idx in splits:
                left = self.searchable_name[:idx].strip()
                right = self.searchable_name[idx + 1 :].strip()
                # use '-' as the new divider since its the most standard
                swapped_name = f"{right} - {left}"
                new_ratio = SequenceMatcher(
                    None, swapped_name, other_track.searchable_name
                ).ratio()
                ratio = max(ratio, new_ratio)

        return ratio


class YTMusic(StreamingService):
    VALID_TRACK_URL_PATTERNS = [
        r"https://music.youtube.com/watch\?v=(?P<trackId>\w+).*",
    ]

    def __init__(self):
        self._client = None

    def __enter__(self):
        self._client = YTMusicClient()
        return self

    def __exit__(self, *args):
        pass

    def get_track_from_trackId(self, trackId):
        # We'll need to switch clients to support this feature
        raise StreamingServiceActionNotSupportedError()

    def search_tracks(self, q, max_results=None):
        del max_results  # unused, not available through client

        tracks = []
        for search_result in self._client.search(q, filter="songs"):
            track = search_result
            ytm_track = YTMusicTrack(
                track["title"], track["artists"][0]["name"], track["videoId"]
            )
            tracks.append(ytm_track)
        return tracks


if __name__ == "__main__":
    """Integration Tests"""
    with YTMusic() as ytm:
        track = ytm.search_one_track("G.o.a.t polyphia")
        print(track)
        trackId = YTMusic.get_trackId_from_url(track.share_link())
        print(trackId)
        try:
            track = ytm.get_track_from_trackId(trackId)
            print(track)
            print(track.share_link())
        except StreamingServiceActionNotSupportedError:
            print("StreamingServiceActionNotSupportedError")
