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

        # r"\s\(?(HD\s?)?((with |w\/ )?lyrics)?\)?$"

        mock_sst.title = "Song (HD With Lyrics)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (HD W/ Lyrics)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (With Lyrics)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (W/ Lyrics)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        # r"\s\[?(HD\s?)?((with |w\/ )?lyrics)?\]?$"

        mock_sst.title = "Song [HD With Lyrics]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [HD W/ Lyrics]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [With Lyrics]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [W/ Lyrics]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        # r"\((Official\s)?(Music\s|Lyric\s)?(Video|Movie|Audio)\)"

        mock_sst.title = "Song (Official Music Video)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Official Music Movie)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Official Music Audio)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Official Lyric Video)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Official Lyric Movie)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Official Lyric Audio)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Official Video)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Official Movie)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Official Audio)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Music Video)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Music Movie)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Music Audio)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Lyric Video)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Lyric Movie)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Lyric Audio)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Video)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Movie)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Audio)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        # r"\[(Official\s)?(Music\s|Lyric\s)?(Video|Movie|Audio)\]"

        mock_sst.title = "Song [Official Music Video]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Official Music Movie]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Official Music Audio]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Official Lyric Video]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Official Lyric Movie]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Official Lyric Audio]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Official Video]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Official Movie]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Official Audio]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Music Video]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Music Movie]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Music Audio]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Lyric Video]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Lyric Movie]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Lyric Audio]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Video]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Movie]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Audio]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        # r"\s\(.*Live (at|on).*\)"

        mock_sst.title = "Song (Live)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Live at Bonnaroo)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Live on Stage)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song (Recorded Live in San Francisco)"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        # r"\s\[.*Live (at|on).*\]"

        mock_sst.title = "Song [Live]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Live at Bonnaroo]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Live on Stage]"
        self.assertEqual(mock_sst.cleaned_title, "Song")

        mock_sst.title = "Song [Recorded Live in San Francisco]"
        self.assertEqual(mock_sst.cleaned_title, "Song")
