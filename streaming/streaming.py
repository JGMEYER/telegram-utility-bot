from abc import ABCMeta, abstractmethod, abstractproperty

class StreamingService(object, metaclass=ABCMeta):
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, *args):
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

    @abstractmethod
    def supports_url(self, url):
        pass

    @abstractmethod
    def get_track_name_from_url(self, url):
        pass

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
