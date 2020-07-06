DIVIDERS = [("(", ")"), ("[", "]")]

WORD1 = ["Official ", ""]
WORD2 = ["Music ", "Lyric ", ""]
WORD3 = ["Video", "Movie", "Audio"]


for i in range(2):
    for a in WORD1:
        for b in WORD2:
            for c in WORD3:
                print(
                    f'mock_sst.title = "Song {DIVIDERS[i][0]}{a}{b}{c}{DIVIDERS[i][1]}"\n'
                    f'self.assertEqual(mock_sst.cleaned_title, "Song")\n'
                )
