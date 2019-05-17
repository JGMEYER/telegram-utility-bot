import os

import httplib2
from googleapiclient.discovery import build

# Log all request/response headers and bodies
httplib2.debuglevel = 4

def search_youtube(q, max_results):
    youtube = build('youtube', 'v3',
      developerKey=os.environ.get('YOUTUBE_API_KEY'))

    search_response = youtube.search().list(
        q=q,
        part="id,snippet",
        maxResults=max_results,
    ).execute()

    videos = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                       search_result["id"]["videoId"]))
    return videos

if __name__ == '__main__':
    print(search_youtube(q="G.o.a.t polyphia", max_results=5))
