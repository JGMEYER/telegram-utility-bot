import html
import re
from abc import ABCMeta, abstractmethod, abstractproperty
from difflib import SequenceMatcher


class StreamingServiceActionNotSupportedError(Exception):
    """Error raised when a StreamingService cannot support an action"""

    pass


class StreamingService(object, metaclass=ABCMeta):
    @abstractproperty
    def VALID_TRACK_URL_PATTERNS(self):
        """List of string patterns of supported urls. Url must include matching
        group for trackId.
        e.g. "(?P<trackId>\w+)"
        """  # noqa: W605
        raise NotImplementedError

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, *args):
        pass

    @classmethod
    def supports_track_url(cls, url):
        for pattern in cls.VALID_TRACK_URL_PATTERNS:
            if re.search(pattern, url):
                return True
        return False

    @classmethod
    def get_trackId_from_url(cls, url):
        for pattern in cls.VALID_TRACK_URL_PATTERNS:
            match = re.search(pattern, url)
            if match:
                return match.group("trackId")

    @abstractmethod
    def get_track_from_trackId(self, trackId):
        """Returns StreamingServiceTrack or None"""
        pass

    @abstractmethod
    def search_tracks(self, q, max_results):
        """
        Returns list of StreamingServiceTrack or empty list.
        Child class should define a default for max_results.
        """
        pass

    def search_one_track(self, q):
        tracks = self.search_tracks(q, max_results=1)
        return tracks[0] if tracks else None


class StreamingServiceTrack(metaclass=ABCMeta):
    def __str__(self):
        return (
            f"{self.__class__.__name__}: '{self.name}' - {self.artist} "
            f"({self.id})"
        )

    # Expressions that impact our ability to effectively match between
    # different services.
    TITLE_EXCLUDE_EXPRESSIONS = [
        r"\s\(?(HD\s?)?((with |w\/ )?lyrics)?\)?$",  # ()'s
        r"\s\[?(HD\s?)?((with |w\/ )?lyrics)?\]?$",  # []'s
        r"\((Official\s)?(Music\s|Lyric\s)?(Video|Movie|Audio)\)",  # ()'s
        r"\[(Official\s)?(Music\s|Lyric\s)?(Video|Movie|Audio)\]",  # []'s
        r"\s\(.*Live( at| on| in)?.*\)",  # ()'s
        r"\s\[.*Live( at| on| in)?.*\]",  # []'s
        r"\s\((Original|Official)( Mix)?\)",  # ()'s
        r"\s\[(Original|Official)( Mix)?\]",  # []'s
        r"\s\(Remaster(ed)?\)",  # ()'s
        r"\s\[Remaster(ed)?\]",  # []'s
        r"\s\((Feat\.?|Featuring)\s.*\)",  # ()'s
        r"\s\[(Feat\.?|Featuring)\s.*\]",  # []'s
    ]

    @abstractproperty
    def title(self):
        raise NotImplementedError

    @abstractproperty
    def artist(self):
        raise NotImplementedError

    @abstractproperty
    def id(self):
        raise NotImplementedError

    # TODO lazy load or make more efficient?
    @property
    def cleaned_title(self):
        cleaned_title = html.unescape(self.title)
        # Remove terms that negatively impact search between services
        for exp in self.TITLE_EXCLUDE_EXPRESSIONS:
            cleaned_title = re.sub(exp, "", cleaned_title, flags=re.IGNORECASE)
        return cleaned_title.strip()

    @property
    def searchable_name(self):
        return f"{self.cleaned_title} - {self.artist}"

    @abstractmethod
    def share_link(self):
        """Returns a sharable link to the track"""
        pass

    def similarity_ratio(self, other_track):
        """Returns ratio of similarity between track names"""
        return SequenceMatcher(
            None, self.searchable_name, other_track.searchable_name
        ).ratio()
