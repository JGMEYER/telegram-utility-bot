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

        def _assert_cleaned(title, target="Title"):
            old_title = mock_sst.title
            mock_sst.title = title
            self.assertEqual(mock_sst.cleaned_title, target)
            mock_sst.title = old_title

        # r"\s\(?(HD )?((with |w\/ )?lyrics)?\)?$"

        _assert_cleaned("Title (HD With Lyrics)")
        _assert_cleaned("Title (HD W/ Lyrics)")
        _assert_cleaned("Title (With Lyrics)")
        _assert_cleaned("Title (W/ Lyrics)")

        # r"\s\[?(HD )?((with |w\/ )?lyrics)?\]?$"

        _assert_cleaned("Title [HD With Lyrics]")
        _assert_cleaned("Title [HD W/ Lyrics]")
        _assert_cleaned("Title [With Lyrics]")
        _assert_cleaned("Title [W/ Lyrics]")

        # r"\((Official )?(Music |Lyric )?(Video|Movie|Audio)\)"

        _assert_cleaned("Title (Official Unreleased Music Video)")
        _assert_cleaned("Title (Official Unreleased Music Movie)")
        _assert_cleaned("Title (Official Unreleased Music Audio)")
        _assert_cleaned("Title (Official Unreleased Lyric Video)")
        _assert_cleaned("Title (Official Unreleased Lyric Movie)")
        _assert_cleaned("Title (Official Unreleased Lyric Audio)")
        _assert_cleaned("Title (Official Unreleased Video)")
        _assert_cleaned("Title (Official Unreleased Movie)")
        _assert_cleaned("Title (Official Unreleased Audio)")
        _assert_cleaned("Title (Official Music Video)")
        _assert_cleaned("Title (Official Music Movie)")
        _assert_cleaned("Title (Official Music Audio)")
        _assert_cleaned("Title (Official Lyric Video)")
        _assert_cleaned("Title (Official Lyric Movie)")
        _assert_cleaned("Title (Official Lyric Audio)")
        _assert_cleaned("Title (Official Video)")
        _assert_cleaned("Title (Official Movie)")
        _assert_cleaned("Title (Official Audio)")
        _assert_cleaned("Title (New Unreleased Music Video)")
        _assert_cleaned("Title (New Unreleased Music Movie)")
        _assert_cleaned("Title (New Unreleased Music Audio)")
        _assert_cleaned("Title (New Unreleased Lyric Video)")
        _assert_cleaned("Title (New Unreleased Lyric Movie)")
        _assert_cleaned("Title (New Unreleased Lyric Audio)")
        _assert_cleaned("Title (New Unreleased Video)")
        _assert_cleaned("Title (New Unreleased Movie)")
        _assert_cleaned("Title (New Unreleased Audio)")
        _assert_cleaned("Title (New Music Video)")
        _assert_cleaned("Title (New Music Movie)")
        _assert_cleaned("Title (New Music Audio)")
        _assert_cleaned("Title (New Lyric Video)")
        _assert_cleaned("Title (New Lyric Movie)")
        _assert_cleaned("Title (New Lyric Audio)")
        _assert_cleaned("Title (New Video)")
        _assert_cleaned("Title (New Movie)")
        _assert_cleaned("Title (New Audio)")
        _assert_cleaned("Title (Unreleased Music Video)")
        _assert_cleaned("Title (Unreleased Music Movie)")
        _assert_cleaned("Title (Unreleased Music Audio)")
        _assert_cleaned("Title (Unreleased Lyric Video)")
        _assert_cleaned("Title (Unreleased Lyric Movie)")
        _assert_cleaned("Title (Unreleased Lyric Audio)")
        _assert_cleaned("Title (Unreleased Video)")
        _assert_cleaned("Title (Unreleased Movie)")
        _assert_cleaned("Title (Unreleased Audio)")
        _assert_cleaned("Title (Music Video)")
        _assert_cleaned("Title (Music Movie)")
        _assert_cleaned("Title (Music Audio)")
        _assert_cleaned("Title (Lyric Video)")
        _assert_cleaned("Title (Lyric Movie)")
        _assert_cleaned("Title (Lyric Audio)")
        _assert_cleaned("Title (Video)")
        _assert_cleaned("Title (Movie)")
        _assert_cleaned("Title (Audio)")

        # r"\[(Official )?(Music |Lyric )?(Video|Movie|Audio)\]"

        _assert_cleaned("Title [Official Unreleased Music Video]")
        _assert_cleaned("Title [Official Unreleased Music Movie]")
        _assert_cleaned("Title [Official Unreleased Music Audio]")
        _assert_cleaned("Title [Official Unreleased Lyric Video]")
        _assert_cleaned("Title [Official Unreleased Lyric Movie]")
        _assert_cleaned("Title [Official Unreleased Lyric Audio]")
        _assert_cleaned("Title [Official Unreleased Video]")
        _assert_cleaned("Title [Official Unreleased Movie]")
        _assert_cleaned("Title [Official Unreleased Audio]")
        _assert_cleaned("Title [Official Music Video]")
        _assert_cleaned("Title [Official Music Movie]")
        _assert_cleaned("Title [Official Music Audio]")
        _assert_cleaned("Title [Official Lyric Video]")
        _assert_cleaned("Title [Official Lyric Movie]")
        _assert_cleaned("Title [Official Lyric Audio]")
        _assert_cleaned("Title [Official Video]")
        _assert_cleaned("Title [Official Movie]")
        _assert_cleaned("Title [Official Audio]")
        _assert_cleaned("Title [New Unreleased Music Video]")
        _assert_cleaned("Title [New Unreleased Music Movie]")
        _assert_cleaned("Title [New Unreleased Music Audio]")
        _assert_cleaned("Title [New Unreleased Lyric Video]")
        _assert_cleaned("Title [New Unreleased Lyric Movie]")
        _assert_cleaned("Title [New Unreleased Lyric Audio]")
        _assert_cleaned("Title [New Unreleased Video]")
        _assert_cleaned("Title [New Unreleased Movie]")
        _assert_cleaned("Title [New Unreleased Audio]")
        _assert_cleaned("Title [New Music Video]")
        _assert_cleaned("Title [New Music Movie]")
        _assert_cleaned("Title [New Music Audio]")
        _assert_cleaned("Title [New Lyric Video]")
        _assert_cleaned("Title [New Lyric Movie]")
        _assert_cleaned("Title [New Lyric Audio]")
        _assert_cleaned("Title [New Video]")
        _assert_cleaned("Title [New Movie]")
        _assert_cleaned("Title [New Audio]")
        _assert_cleaned("Title [Unreleased Music Video]")
        _assert_cleaned("Title [Unreleased Music Movie]")
        _assert_cleaned("Title [Unreleased Music Audio]")
        _assert_cleaned("Title [Unreleased Lyric Video]")
        _assert_cleaned("Title [Unreleased Lyric Movie]")
        _assert_cleaned("Title [Unreleased Lyric Audio]")
        _assert_cleaned("Title [Unreleased Video]")
        _assert_cleaned("Title [Unreleased Movie]")
        _assert_cleaned("Title [Unreleased Audio]")
        _assert_cleaned("Title [Music Video]")
        _assert_cleaned("Title [Music Movie]")
        _assert_cleaned("Title [Music Audio]")
        _assert_cleaned("Title [Lyric Video]")
        _assert_cleaned("Title [Lyric Movie]")
        _assert_cleaned("Title [Lyric Audio]")
        _assert_cleaned("Title [Video]")
        _assert_cleaned("Title [Movie]")
        _assert_cleaned("Title [Audio]")

        # r"\| (Official )?(Music |Lyric )?(Video|Movie|Audio)"

        _assert_cleaned("Title | Official Music Video")
        _assert_cleaned("Title | Official Music Movie")
        _assert_cleaned("Title | Official Music Audio")
        _assert_cleaned("Title | Official Lyric Video")
        _assert_cleaned("Title | Official Lyric Movie")
        _assert_cleaned("Title | Official Lyric Audio")
        _assert_cleaned("Title | Official Video")
        _assert_cleaned("Title | Official Movie")
        _assert_cleaned("Title | Official Audio")
        _assert_cleaned("Title | Music Video")
        _assert_cleaned("Title | Music Movie")
        _assert_cleaned("Title | Music Audio")
        _assert_cleaned("Title | Lyric Video")
        _assert_cleaned("Title | Lyric Movie")
        _assert_cleaned("Title | Lyric Audio")
        _assert_cleaned("Title | Video")
        _assert_cleaned("Title | Movie")
        _assert_cleaned("Title | Audio")
        _assert_cleaned("Title - Official Music Video")
        _assert_cleaned("Title - Official Music Movie")
        _assert_cleaned("Title - Official Music Audio")
        _assert_cleaned("Title - Official Lyric Video")
        _assert_cleaned("Title - Official Lyric Movie")
        _assert_cleaned("Title - Official Lyric Audio")
        _assert_cleaned("Title - Official Video")
        _assert_cleaned("Title - Official Movie")
        _assert_cleaned("Title - Official Audio")
        _assert_cleaned("Title - Music Video")
        _assert_cleaned("Title - Music Movie")
        _assert_cleaned("Title - Music Audio")
        _assert_cleaned("Title - Lyric Video")
        _assert_cleaned("Title - Lyric Movie")
        _assert_cleaned("Title - Lyric Audio")
        _assert_cleaned("Title - Video")
        _assert_cleaned("Title - Movie")
        _assert_cleaned("Title - Audio")
        _assert_cleaned("Title Official Music Video")
        _assert_cleaned("Title Official Music Movie")
        _assert_cleaned("Title Official Music Audio")
        _assert_cleaned("Title Official Lyric Video")
        _assert_cleaned("Title Official Lyric Movie")
        _assert_cleaned("Title Official Lyric Audio")
        _assert_cleaned("Title Official Video")
        _assert_cleaned("Title Official Movie")
        _assert_cleaned("Title Official Audio")
        _assert_cleaned("Title Music Video")
        _assert_cleaned("Title Music Movie")
        _assert_cleaned("Title Music Audio")
        _assert_cleaned("Title Lyric Video")
        _assert_cleaned("Title Lyric Movie")
        _assert_cleaned("Title Lyric Audio")
        _assert_cleaned("Title Video")
        _assert_cleaned("Title Movie")
        _assert_cleaned("Title Audio")

        # r"\s\(.*Live( at| on| in)?.*\)"

        _assert_cleaned("Title (Live)")
        _assert_cleaned("Title (Live at Bonnaroo)")
        _assert_cleaned("Title (Live on Stage)")
        _assert_cleaned("Title (Recorded Live in San Francisco)")

        # r"\s\[.*Live( at| on| in)?.*\]"

        _assert_cleaned("Title [Live]")
        _assert_cleaned("Title [Live at Bonnaroo]")
        _assert_cleaned("Title [Live on Stage]")
        _assert_cleaned("Title [Recorded Live in San Francisco]")

        # r"\s\| Live( at| on| in)?.*$"

        _assert_cleaned("Title | Live")
        _assert_cleaned("Title | Live at Bonnaroo")
        _assert_cleaned("Title | Live on Stage")
        _assert_cleaned("Title | Live on Stage | 2020")
        _assert_cleaned(
            "Title | Recorded Live in San Francisco",
            "Title | Recorded Live in San Francisco",
        )  # does not match regex

        # r"\s\((Original|Official)( Mix)?\)"

        _assert_cleaned("Title (Original)")
        _assert_cleaned("Title (Official)")
        _assert_cleaned("Title (Original Mix)")
        _assert_cleaned("Title (Official Mix)")

        # r"\s\[(Original|Official)( Mix)?\]"

        _assert_cleaned("Title [Original]")
        _assert_cleaned("Title [Official]")
        _assert_cleaned("Title [Original Mix]")
        _assert_cleaned("Title [Official Mix]")

        # r"\s\(.*Remaster(ed)?.*\)"

        _assert_cleaned("Title (Remaster)")
        _assert_cleaned("Title (2011 Remaster)")
        _assert_cleaned("Title (Remastered)")
        _assert_cleaned("Title (Remastered 2011)")

        # r"\s\[.*Remaster(ed)?.*\]"

        _assert_cleaned("Title [Remaster]")
        _assert_cleaned("Title [2011 Remaster]")
        _assert_cleaned("Title [Remastered]")
        _assert_cleaned("Title [Remastered 2011]")

        # r"(\| |\- ).*Remaster(ed)?[^\||^\-]*"

        _assert_cleaned("Title - Remaster - Artist", "Title - Artist")
        _assert_cleaned("Title - 2020 Remaster - Artist", "Title - Artist")
        _assert_cleaned("Title - Remastered - Artist", "Title - Artist")
        _assert_cleaned("Title - Remastered 2020 - Artist", "Title - Artist")
        _assert_cleaned("Title | Remaster | Artist", "Title | Artist")
        _assert_cleaned("Title | 2020 Remaster | Artist", "Title | Artist")
        _assert_cleaned("Title | Remastered | Artist", "Title | Artist")
        _assert_cleaned("Title | Remastered 2020 | Artist", "Title | Artist")

        # r"\s(\| |- ).*Remaster(ed)?.*$"

        _assert_cleaned("Title | Remaster")
        _assert_cleaned("Title | 2020 Remaster")
        _assert_cleaned("Title | Remastered")
        _assert_cleaned("Title | Remastered 2020")
        _assert_cleaned("Title - Remaster")
        _assert_cleaned("Title - 2020 Remaster")
        _assert_cleaned("Title - Remastered")
        _assert_cleaned("Title - Remastered 2020")

        # r"Remaster(ed)?[\s]?",

        _assert_cleaned("Title Remaster")
        _assert_cleaned("Title Remastered")

        # very complicated cases to manage, we don't want to accidentally lose
        # information from removing anything before or after "Remaster"
        _assert_cleaned("Title Remaster 2020", "Title 2020")
        _assert_cleaned("Title Remastered 2020", "Title 2020")
        _assert_cleaned("Title 2020 Remaster", "Title 2020")
        _assert_cleaned("Title 2020 Remastered", "Title 2020")

        # r"\s\((Ft\.?|Feat\.?|Featuring)\:?\s.*\)"

        _assert_cleaned("Title [Ft Calvin & Hobbes]")
        _assert_cleaned("Title (Ft. Calvin & Hobbes)")
        _assert_cleaned("Title (Ft: Calvin & Hobbes)")
        _assert_cleaned("Title (Feat Calvin & Hobbes)")
        _assert_cleaned("Title (Feat. Calvin & Hobbes)")
        _assert_cleaned("Title (Feat: Calvin & Hobbes)")
        _assert_cleaned("Title (Featuring Calvin & Hobbes)")
        _assert_cleaned("Title (Featuring: Calvin & Hobbes)")

        # r"\s\[(Feat\.?|Featuring)\:?\s.*\]"

        _assert_cleaned("Title [Ft Calvin & Hobbes]")
        _assert_cleaned("Title [Ft. Calvin & Hobbes]")
        _assert_cleaned("Title [Ft: Calvin & Hobbes]")
        _assert_cleaned("Title [Feat Calvin & Hobbes]")
        _assert_cleaned("Title [Feat. Calvin & Hobbes]")
        _assert_cleaned("Title [Feat: Calvin & Hobbes]")
        _assert_cleaned("Title [Featuring Calvin & Hobbes]")
        _assert_cleaned("Title [Featuring: Calvin & Hobbes]")

        # r"\s(Ft\.?|Feat\.?|Featuring)\:?\s.*"

        _assert_cleaned("Title Ft Calvin & Hobbes")
        _assert_cleaned("Title Ft. Calvin & Hobbes")
        _assert_cleaned("Title Ft: Calvin & Hobbes")
        _assert_cleaned("Title Feat Calvin & Hobbes")
        _assert_cleaned("Title Feat. Calvin & Hobbes")
        _assert_cleaned("Title Feat: Calvin & Hobbes")
        _assert_cleaned("Title Featuring Calvin & Hobbes")
        _assert_cleaned("Title Featuring: Calvin & Hobbes")

        # r"\s\(Visuali[sz]er\)"

        _assert_cleaned("Title (Visualiser)")
        _assert_cleaned("Title (Visualizer)")

        # r"\s\[Visuali[sz]er\]"

        _assert_cleaned("Title [Visualiser]")
        _assert_cleaned("Title [Visualizer]")

    def test_cleaned_artist(self):
        mock_sst = MockStreamingServiceTrack(None, None, None)

        def _assert_cleaned(artist, target="Artist"):
            old_artist = mock_sst.artist
            mock_sst.artist = artist
            self.assertEqual(mock_sst.cleaned_artist, target)
            mock_sst.artist = old_artist

        # r"\s\-\sTopic$"
        _assert_cleaned("Artist - Topic")

    def test_searchable_name(self):
        """Test searchable names on real-world examples"""

        mock_sst = MockStreamingServiceTrack(None, None, None)

        def _assert_searchable(title, artist, expected):
            mock_sst.artist = artist
            mock_sst.title = title
            self.assertEqual(mock_sst.searchable_name, expected)
            mock_sst.artist = None
            mock_sst.title = None

        mock_sst = MockStreamingServiceTrack(
            "Stars Have No Names (they just shine) (feat: Nick Arnold & Chrissy Dunn)",
            "Bootsy Collins",
            "stars have no names (they just shine) - bootsy collins",
        )
