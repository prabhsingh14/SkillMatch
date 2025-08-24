import requests
from django.conf import settings

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"

def search_youtube_videos(query, max_results=5):
    params = {
        "part": "snippet",
        "q": query,
        "maxResults": max_results,
        "key": settings.YOUTUBE_API_KEY
    }

    response = requests.get(YOUTUBE_API_URL, params=params)
    response.raise_for_status()
    data = response.json()

    videos = []
    for item in data.get("items", []):
        videos.append({
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
            "channel": item["snippet"]["channelTitle"]
        })

    return videos