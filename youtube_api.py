import re
import requests

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"


def extract_video_id(url):
    """Handles youtube.com/watch?v=, youtu.be/, and shorts URLs."""
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"(?:embed\/)([0-9A-Za-z_-]{11})",
        r"(?:shorts\/)([0-9A-Za-z_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def fetch_video_details(video_id, api_key):
    """Returns title, thumbnail, tags, view/like count for a video."""
    params = {"part": "snippet,statistics", "id": video_id, "key": api_key}
    resp = requests.get(f"{YOUTUBE_API_URL}/videos", params=params)
    resp.raise_for_status()
    data = resp.json()

    if not data.get("items"):
        return None

    snippet = data["items"][0]["snippet"]
    stats = data["items"][0]["statistics"]

    return {
        "title": snippet.get("title"),
        "thumbnail": snippet["thumbnails"]["high"]["url"],
        "tags": snippet.get("tags", []),
        "view_count": stats.get("viewCount", "N/A"),
        "like_count": stats.get("likeCount", "N/A"),
    }


def fetch_comments(video_id, api_key, max_comments=500):
    """Fetches up to max_comments top-level comments, paginated."""
    comments = []
    page_token = None

    while len(comments) < max_comments:
        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": 100,
            "textFormat": "plainText",
            "key": api_key,
        }
        if page_token:
            params["pageToken"] = page_token

        resp = requests.get(f"{YOUTUBE_API_URL}/commentThreads", params=params)
        if resp.status_code != 200:
            break  # comments may be disabled

        data = resp.json()
        for item in data.get("items", []):
            text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(text)

        page_token = data.get("nextPageToken")
        if not page_token:
            break

    return comments[:max_comments]