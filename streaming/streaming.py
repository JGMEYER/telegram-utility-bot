from abc import ABCMeta, abstractmethod, abstractproperty
import re

class StreamingService(object, metaclass=ABCMeta):
    @abstractproperty
    def VALID_TRACK_URL_PATTERNS(self):
        """
        List of string patterns of supported urls.
        Url must include matching group for trackId.
        e.g. "(?P<trackId>\w+)"
        """
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
                return match.group('trackId')

    @abstractmethod
    def get_track_from_trackId(self, trackId):
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
        return f"{self.__class__.__name__}: '{self.name}' - {self.artist} ({self.id})"

    @abstractproperty
    def name(self):
        raise NotImplementedError

    @abstractproperty
    def artist(self):
        raise NotImplementedError

    @abstractproperty
    def id(self):
        raise NotImplementedError

    @property
    def searchable_name(self):
        return f"{self.name} {self.artist}"

    @abstractmethod
    def share_link(self):
        """Returns a sharable link to the track"""
        pass
