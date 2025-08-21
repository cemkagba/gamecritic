
from googleapiclient.discovery import build
import os
<<<<<<< HEAD
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
=======

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
>>>>>>> 9d50b2831be56ef54576e484e5000b1b8993be64

def _pick_public_embeddable(video_ids):
    """Fetch video status with videos.list and return the first ID that is public + embeddable."""
    
    if not video_ids:
        return None
    details = youtube.videos().list(
        id=",".join(video_ids),
        part="status,snippet",
        maxResults=len(video_ids)
    ).execute()

<<<<<<< HEAD
    for v in details.get("items", []):
        st = v.get("status", {})
        if st.get("privacyStatus") == "public" and st.get("embeddable", False):
=======
    request = youtube.search().list(
        q=f"{querry} official trailer",
        part='snippet',
        type='video',
        maxResults=max_result
    )

    response = request.execute()
    return [
        {
>>>>>>> 9d50b2831be56ef54576e484e5000b1b8993be64
            
            return {
                "title": v["snippet"]["title"],
                "video_id": v["id"],                         
            }
    return None

def _search_one(query_text, max_try=5):
    """Aramadan birkaç aday çek, sonra public+embeddable ilkini seç."""
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



