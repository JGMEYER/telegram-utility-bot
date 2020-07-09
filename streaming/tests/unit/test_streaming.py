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

        def _assert_cleaned(title, target="Song"):
            old_title = mock_sst.title
            mock_sst.title = title
            self.assertEqual(mock_sst.cleaned_title, target)
            mock_sst.title = old_title

        # r"\s\(?(HD )?((with |w\/ )?lyrics)?\)?$"

        _assert_cleaned("Song (HD With Lyrics)")
        _assert_cleaned("Song (HD W/ Lyrics)")
        _assert_cleaned("Song (With Lyrics)")
        _assert_cleaned("Song (W/ Lyrics)")

        # r"\s\[?(HD )?((with |w\/ )?lyrics)?\]?$"

        _assert_cleaned("Song [HD With Lyrics]")
        _assert_cleaned("Song [HD W/ Lyrics]")
        _assert_cleaned("Song [With Lyrics]")
        _assert_cleaned("Song [W/ Lyrics]")

        # r"\((Official )?(Music |Lyric )?(Video|Movie|Audio)\)"

        _assert_cleaned("Song (Official Unreleased Music Video)")
        _assert_cleaned("Song (Official Unreleased Music Movie)")
        _assert_cleaned("Song (Official Unreleased Music Audio)")
        _assert_cleaned("Song (Official Unreleased Lyric Video)")
        _assert_cleaned("Song (Official Unreleased Lyric Movie)")
        _assert_cleaned("Song (Official Unreleased Lyric Audio)")
        _assert_cleaned("Song (Official Unreleased Video)")
        _assert_cleaned("Song (Official Unreleased Movie)")
        _assert_cleaned("Song (Official Unreleased Audio)")
        _assert_cleaned("Song (Official Music Video)")
        _assert_cleaned("Song (Official Music Movie)")
        _assert_cleaned("Song (Official Music Audio)")
        _assert_cleaned("Song (Official Lyric Video)")
        _assert_cleaned("Song (Official Lyric Movie)")
        _assert_cleaned("Song (Official Lyric Audio)")
        _assert_cleaned("Song (Official Video)")
        _assert_cleaned("Song (Official Movie)")
        _assert_cleaned("Song (Official Audio)")
        _assert_cleaned("Song (New Unreleased Music Video)")
        _assert_cleaned("Song (New Unreleased Music Movie)")
        _assert_cleaned("Song (New Unreleased Music Audio)")
        _assert_cleaned("Song (New Unreleased Lyric Video)")
        _assert_cleaned("Song (New Unreleased Lyric Movie)")
        _assert_cleaned("Song (New Unreleased Lyric Audio)")
        _assert_cleaned("Song (New Unreleased Video)")
        _assert_cleaned("Song (New Unreleased Movie)")
        _assert_cleaned("Song (New Unreleased Audio)")
        _assert_cleaned("Song (New Music Video)")
        _assert_cleaned("Song (New Music Movie)")
        _assert_cleaned("Song (New Music Audio)")
        _assert_cleaned("Song (New Lyric Video)")
        _assert_cleaned("Song (New Lyric Movie)")
        _assert_cleaned("Song (New Lyric Audio)")
        _assert_cleaned("Song (New Video)")
        _assert_cleaned("Song (New Movie)")
        _assert_cleaned("Song (New Audio)")
        _assert_cleaned("Song (Unreleased Music Video)")
        _assert_cleaned("Song (Unreleased Music Movie)")
        _assert_cleaned("Song (Unreleased Music Audio)")
        _assert_cleaned("Song (Unreleased Lyric Video)")
        _assert_cleaned("Song (Unreleased Lyric Movie)")
        _assert_cleaned("Song (Unreleased Lyric Audio)")
        _assert_cleaned("Song (Unreleased Video)")
        _assert_cleaned("Song (Unreleased Movie)")
        _assert_cleaned("Song (Unreleased Audio)")
        _assert_cleaned("Song (Music Video)")
        _assert_cleaned("Song (Music Movie)")
        _assert_cleaned("Song (Music Audio)")
        _assert_cleaned("Song (Lyric Video)")
        _assert_cleaned("Song (Lyric Movie)")
        _assert_cleaned("Song (Lyric Audio)")
        _assert_cleaned("Song (Video)")
        _assert_cleaned("Song (Movie)")
        _assert_cleaned("Song (Audio)")

        # r"\[(Official )?(Music |Lyric )?(Video|Movie|Audio)\]"

        _assert_cleaned("Song [Official Unreleased Music Video]")
        _assert_cleaned("Song [Official Unreleased Music Movie]")
        _assert_cleaned("Song [Official Unreleased Music Audio]")
        _assert_cleaned("Song [Official Unreleased Lyric Video]")
        _assert_cleaned("Song [Official Unreleased Lyric Movie]")
        _assert_cleaned("Song [Official Unreleased Lyric Audio]")
        _assert_cleaned("Song [Official Unreleased Video]")
        _assert_cleaned("Song [Official Unreleased Movie]")
        _assert_cleaned("Song [Official Unreleased Audio]")
        _assert_cleaned("Song [Official Music Video]")
        _assert_cleaned("Song [Official Music Movie]")
        _assert_cleaned("Song [Official Music Audio]")
        _assert_cleaned("Song [Official Lyric Video]")
        _assert_cleaned("Song [Official Lyric Movie]")
        _assert_cleaned("Song [Official Lyric Audio]")
        _assert_cleaned("Song [Official Video]")
        _assert_cleaned("Song [Official Movie]")
        _assert_cleaned("Song [Official Audio]")
        _assert_cleaned("Song [New Unreleased Music Video]")
        _assert_cleaned("Song [New Unreleased Music Movie]")
        _assert_cleaned("Song [New Unreleased Music Audio]")
        _assert_cleaned("Song [New Unreleased Lyric Video]")
        _assert_cleaned("Song [New Unreleased Lyric Movie]")
        _assert_cleaned("Song [New Unreleased Lyric Audio]")
        _assert_cleaned("Song [New Unreleased Video]")
        _assert_cleaned("Song [New Unreleased Movie]")
        _assert_cleaned("Song [New Unreleased Audio]")
        _assert_cleaned("Song [New Music Video]")
        _assert_cleaned("Song [New Music Movie]")
        _assert_cleaned("Song [New Music Audio]")
        _assert_cleaned("Song [New Lyric Video]")
        _assert_cleaned("Song [New Lyric Movie]")
        _assert_cleaned("Song [New Lyric Audio]")
        _assert_cleaned("Song [New Video]")
        _assert_cleaned("Song [New Movie]")
        _assert_cleaned("Song [New Audio]")
        _assert_cleaned("Song [Unreleased Music Video]")
        _assert_cleaned("Song [Unreleased Music Movie]")
        _assert_cleaned("Song [Unreleased Music Audio]")
        _assert_cleaned("Song [Unreleased Lyric Video]")
        _assert_cleaned("Song [Unreleased Lyric Movie]")
        _assert_cleaned("Song [Unreleased Lyric Audio]")
        _assert_cleaned("Song [Unreleased Video]")
        _assert_cleaned("Song [Unreleased Movie]")
        _assert_cleaned("Song [Unreleased Audio]")
        _assert_cleaned("Song [Music Video]")
        _assert_cleaned("Song [Music Movie]")
        _assert_cleaned("Song [Music Audio]")
        _assert_cleaned("Song [Lyric Video]")
        _assert_cleaned("Song [Lyric Movie]")
        _assert_cleaned("Song [Lyric Audio]")
        _assert_cleaned("Song [Video]")
        _assert_cleaned("Song [Movie]")
        _assert_cleaned("Song [Audio]")

        # r"\| (Official )?(Music |Lyric )?(Video|Movie|Audio)"

        _assert_cleaned("Song | Official Music Video")
        _assert_cleaned("Song | Official Music Movie")
        _assert_cleaned("Song | Official Music Audio")
        _assert_cleaned("Song | Official Lyric Video")
        _assert_cleaned("Song | Official Lyric Movie")
        _assert_cleaned("Song | Official Lyric Audio")
        _assert_cleaned("Song | Official Video")
        _assert_cleaned("Song | Official Movie")
        _assert_cleaned("Song | Official Audio")
        _assert_cleaned("Song | Music Video")
        _assert_cleaned("Song | Music Movie")
        _assert_cleaned("Song | Music Audio")
        _assert_cleaned("Song | Lyric Video")
        _assert_cleaned("Song | Lyric Movie")
        _assert_cleaned("Song | Lyric Audio")
        _assert_cleaned("Song | Video")
        _assert_cleaned("Song | Movie")
        _assert_cleaned("Song | Audio")
        _assert_cleaned("Song - Official Music Video")
        _assert_cleaned("Song - Official Music Movie")
        _assert_cleaned("Song - Official Music Audio")
        _assert_cleaned("Song - Official Lyric Video")
        _assert_cleaned("Song - Official Lyric Movie")
        _assert_cleaned("Song - Official Lyric Audio")
        _assert_cleaned("Song - Official Video")
        _assert_cleaned("Song - Official Movie")
        _assert_cleaned("Song - Official Audio")
        _assert_cleaned("Song - Music Video")
        _assert_cleaned("Song - Music Movie")
        _assert_cleaned("Song - Music Audio")
        _assert_cleaned("Song - Lyric Video")
        _assert_cleaned("Song - Lyric Movie")
        _assert_cleaned("Song - Lyric Audio")
        _assert_cleaned("Song - Video")
        _assert_cleaned("Song - Movie")
        _assert_cleaned("Song - Audio")
        _assert_cleaned("Song Official Music Video")
        _assert_cleaned("Song Official Music Movie")
        _assert_cleaned("Song Official Music Audio")
        _assert_cleaned("Song Official Lyric Video")
        _assert_cleaned("Song Official Lyric Movie")
        _assert_cleaned("Song Official Lyric Audio")
        _assert_cleaned("Song Official Video")
        _assert_cleaned("Song Official Movie")
        _assert_cleaned("Song Official Audio")
        _assert_cleaned("Song Music Video")
        _assert_cleaned("Song Music Movie")
        _assert_cleaned("Song Music Audio")
        _assert_cleaned("Song Lyric Video")
        _assert_cleaned("Song Lyric Movie")
        _assert_cleaned("Song Lyric Audio")
        _assert_cleaned("Song Video")
        _assert_cleaned("Song Movie")
        _assert_cleaned("Song Audio")

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

        # r"\s\| Live( at| on| in)?.*$"

        _assert_cleaned("Song | Live")
        _assert_cleaned("Song | Live at Bonnaroo")
        _assert_cleaned("Song | Live on Stage")
        _assert_cleaned("Song | Live on Stage | 2020")
        _assert_cleaned(
            "Song | Recorded Live in San Francisco",
            "Song | Recorded Live in San Francisco",
        )  # does not match regex

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

        # r"\s\(.*Remaster(ed)?.*\)"

        _assert_cleaned("Song (Remaster)")
        _assert_cleaned("Song (2011 Remaster)")
        _assert_cleaned("Song (Remastered)")
        _assert_cleaned("Song (Remastered 2011)")

        # r"\s\[.*Remaster(ed)?.*\]"

        _assert_cleaned("Song [Remaster]")
        _assert_cleaned("Song [2011 Remaster]")
        _assert_cleaned("Song [Remastered]")
        _assert_cleaned("Song [Remastered 2011]")

        # r"(\| |\- ).*Remaster(ed)?[^\||^\-]*"

        _assert_cleaned("Song - Remaster - Artist", "Song - Artist")
        _assert_cleaned("Song - 2020 Remaster - Artist", "Song - Artist")
        _assert_cleaned("Song - Remastered - Artist", "Song - Artist")
        _assert_cleaned("Song - Remastered 2020 - Artist", "Song - Artist")
        _assert_cleaned("Song | Remaster | Artist", "Song | Artist")
        _assert_cleaned("Song | 2020 Remaster | Artist", "Song | Artist")
        _assert_cleaned("Song | Remastered | Artist", "Song | Artist")
        _assert_cleaned("Song | Remastered 2020 | Artist", "Song | Artist")

        # r"\s(\| |- ).*Remaster(ed)?.*$"

        _assert_cleaned("Song | Remaster")
        _assert_cleaned("Song | 2020 Remaster")
        _assert_cleaned("Song | Remastered")
        _assert_cleaned("Song | Remastered 2020")
        _assert_cleaned("Song - Remaster")
        _assert_cleaned("Song - 2020 Remaster")
        _assert_cleaned("Song - Remastered")
        _assert_cleaned("Song - Remastered 2020")

        # r"Remaster(ed)?[\s]?",

        _assert_cleaned("Song Remaster")
        _assert_cleaned("Song Remastered")

        # very complicated casesto manage, we don't want to accidentally lose
        # information from removing anything before or after "Remaster"
        _assert_cleaned("Song Remaster 2020", "Song 2020")
        _assert_cleaned("Song Remastered 2020", "Song 2020")
        _assert_cleaned("Song 2020 Remaster", "Song 2020")
        _assert_cleaned("Song 2020 Remastered", "Song 2020")

        # r"\s\((Ft\.?|Feat\.?|Featuring)\s.*\)"

        _assert_cleaned("Song (Ft. Calvin & Hobbes)")
        _assert_cleaned("Song (Feat Calvin & Hobbes)")
        _assert_cleaned("Song (Feat. Calvin & Hobbes)")
        _assert_cleaned("Song (Featuring Calvin & Hobbes)")

        # r"\s\[(Feat\.?|Featuring)\s.*\]"

        _assert_cleaned("Song [Ft. Calvin & Hobbes]")
        _assert_cleaned("Song [Feat Calvin & Hobbes]")
        _assert_cleaned("Song [Feat. Calvin & Hobbes]")
        _assert_cleaned("Song [Featuring Calvin & Hobbes]")

        # r"\s(Ft\.?|Feat\.?|Featuring)\s.*"

        _assert_cleaned("Song Ft. Calvin & Hobbes")
        _assert_cleaned("Song Feat Calvin & Hobbes")
        _assert_cleaned("Song Feat. Calvin & Hobbes")
        _assert_cleaned("Song Featuring Calvin & Hobbes")

        # r"\s\(New( Unreleased)? Video\)"

        _assert_cleaned("Song (New Video)")
        _assert_cleaned("Song (New Unreleased Video)")

        # r"\s\(New( Unreleased)? Video\)"
        _assert_cleaned("Song [New Video]")
        _assert_cleaned("Song [New Unreleased Video]")
