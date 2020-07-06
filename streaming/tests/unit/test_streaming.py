from unittest import TestCase

from ...streaming import StreamingServiceTrack


class MockStreamingServiceTrack(StreamingServiceTrack):
    """Mock StreamingServiceTrack"""

    title = None
    artist = None
    id = None

    def __init__(self, title, artist, id):
        self.title = title
        self.artist = artist
        self.id = id

    def share_link(self):
        return None


class TestStreamingServiceTrack(TestCase):
    """StreamingServiceTrack Tests"""

    def test_cleaned_title(self):
        mock_sst = MockStreamingServiceTrack(None, None, None)

        def _assert_cleaned(title):
            mock_sst.title = title
            self.assertEqual(mock_sst.cleaned_title, "Song")
            mock_sst.title = None

        # r"\s\(?(HD\s?)?((with |w\/ )?lyrics)?\)?$"

        _assert_cleaned("Song (HD With Lyrics)")
        _assert_cleaned("Song (HD W/ Lyrics)")
        _assert_cleaned("Song (With Lyrics)")
        _assert_cleaned("Song (W/ Lyrics)")

        # r"\s\[?(HD\s?)?((with |w\/ )?lyrics)?\]?$"

        _assert_cleaned("Song [HD With Lyrics]")
        _assert_cleaned("Song [HD W/ Lyrics]")
        _assert_cleaned("Song [With Lyrics]")
        _assert_cleaned("Song [W/ Lyrics]")

        # r"\((Official\s)?(Music\s|Lyric\s)?(Video|Movie|Audio)\)"

        _assert_cleaned("Song (Official Music Video)")
        _assert_cleaned("Song (Official Music Movie)")
        _assert_cleaned("Song (Official Music Audio)")
        _assert_cleaned("Song (Official Lyric Video)")
        _assert_cleaned("Song (Official Lyric Movie)")
        _assert_cleaned("Song (Official Lyric Audio)")
        _assert_cleaned("Song (Official Video)")
        _assert_cleaned("Song (Official Movie)")
        _assert_cleaned("Song (Official Audio)")
        _assert_cleaned("Song (Music Video)")
        _assert_cleaned("Song (Music Movie)")
        _assert_cleaned("Song (Music Audio)")
        _assert_cleaned("Song (Lyric Video)")
        _assert_cleaned("Song (Lyric Movie)")
        _assert_cleaned("Song (Lyric Audio)")
        _assert_cleaned("Song (Video)")
        _assert_cleaned("Song (Movie)")
        _assert_cleaned("Song (Audio)")

        # r"\[(Official\s)?(Music\s|Lyric\s)?(Video|Movie|Audio)\]"

        _assert_cleaned("Song [Official Music Video]")
        _assert_cleaned("Song [Official Music Movie]")
        _assert_cleaned("Song [Official Music Audio]")
        _assert_cleaned("Song [Official Lyric Video]")
        _assert_cleaned("Song [Official Lyric Movie]")
        _assert_cleaned("Song [Official Lyric Audio]")
        _assert_cleaned("Song [Official Video]")
        _assert_cleaned("Song [Official Movie]")
        _assert_cleaned("Song [Official Audio]")
        _assert_cleaned("Song [Music Video]")
        _assert_cleaned("Song [Music Movie]")
        _assert_cleaned("Song [Music Audio]")
        _assert_cleaned("Song [Lyric Video]")
        _assert_cleaned("Song [Lyric Movie]")
        _assert_cleaned("Song [Lyric Audio]")
        _assert_cleaned("Song [Video]")
        _assert_cleaned("Song [Movie]")
        _assert_cleaned("Song [Audio]")

        # r"\s\(.*Live( at| on| in)?.*\)"

        _assert_cleaned("Song (Live)")
        _assert_cleaned("Song (Live at Bonnaroo)")
        _assert_cleaned("Song (Live on Stage)")
        _assert_cleaned("Song (Recorded Live in San Francisco)")

        # r"\s\[.*Live( at| on| in)?.*\]"

        _assert_cleaned("Song [Live]")
        _assert_cleaned("Song [Live at Bonnaroo]")
        _assert_cleaned("Song [Live on Stage]")
        _assert_cleaned("Song [Recorded Live in San Francisco]")

        # r"\s\((Original|Official)( Mix)?\)"

        _assert_cleaned("Song (Original)")
        _assert_cleaned("Song (Official)")
        _assert_cleaned("Song (Original Mix)")
        _assert_cleaned("Song (Official Mix)")

        # r"\s\[(Original|Official)( Mix)?\]"

        _assert_cleaned("Song [Original]")
        _assert_cleaned("Song [Official]")
        _assert_cleaned("Song [Original Mix]")
        _assert_cleaned("Song [Official Mix]")

        # r"\s\(Remaster(ed)?\)"

        _assert_cleaned("Song (Remaster)")
        _assert_cleaned("Song (Remastered)")

        # r"\s\[Remaster(ed)?\]"

        _assert_cleaned("Song [Remaster]")
        _assert_cleaned("Song [Remastered]")

        # r"\s\((Feat\.?|Featuring)\s.*\)"

        _assert_cleaned("Song (Feat Calvin & Hobbes)")
        _assert_cleaned("Song (Feat. Calvin & Hobbes)")
        _assert_cleaned("Song (Featuring Calvin & Hobbes)")

        # r"\s\[(Feat\.?|Featuring)\s.*\]"

        _assert_cleaned("Song [Feat Calvin & Hobbes]")
        _assert_cleaned("Song [Feat. Calvin & Hobbes]")
        _assert_cleaned("Song [Featuring Calvin & Hobbes]")
