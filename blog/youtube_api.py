from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
load_dotenv()
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def _pick_public_embeddable(video_ids):
    """Fetch video status with videos.list and return the first ID that is public + embeddable."""
    # Return the first video that is public and embeddable
    if not video_ids:
        return None
    details = youtube.videos().list(
        id=",".join(video_ids),
        part="status,snippet",
        maxResults=len(video_ids)
    ).execute()


    for v in details.get("items", []):
        st = v.get("status", {})
        if st.get("privacyStatus") == "public" and st.get("embeddable", False):
            
            return {
                "title": v["snippet"]["title"],
                "video_id": v["id"],
            }
    return None


def _search_one(query_text, max_try=5):
    """Fetch several candidates from search, then pick the first public+embeddable one."""
    resp = youtube.search().list(
        q=query_text,
        part="id",
        type="video",
        maxResults=max_try,
        videoEmbeddable="true",
        videoSyndicated="true"
    ).execute()

    ids = [it["id"]["videoId"] for it in resp.get("items", []) if "id" in it and "videoId" in it["id"]]
    if not ids:
        return None
    return _pick_public_embeddable(ids)

def search_trailer(game_title, max_result=1):
    return _search_one(f"{game_title} official trailer", max_try=max(5, max_result))

def search_gameplay(game_title, max_result=1):
    return _search_one(f"{game_title} gameplay", max_try=max(5, max_result))

def search_review(game_title, max_result=1):
    return _search_one(f"{game_title} review", max_try=max(5, max_result))

def search_tips(game_title, max_result=1):
    return _search_one(f"{game_title} tips", max_try=max(5, max_result))



