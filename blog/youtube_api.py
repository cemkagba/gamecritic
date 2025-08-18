from googleapiclient.discovery import build


YOUTUBE_API_KEY = 'AIzaSyAwrgomI9T2pXRZdX6srFfQUSTD1y2CEd8'

def search_trailer(querry,max_result=1):
    youtube = build('youtube','v3',developerKey=YOUTUBE_API_KEY)

    request = youtube.search().list(
        q=f"{querry} trailer",
        part='snippet',
        type='video',
        maxResults=max_result
    )

    response = request.execute()
    return [
        {
            
            'title': item['snippet']['title'],
            'video_id': item['id']['videoId'],
        }
        for item in response.get("items", [])
    ]

def search_gameplay(querry,max_result=1):
    youtube = build('youtube','v3',developerKey=YOUTUBE_API_KEY)

    request = youtube.search().list(
        q=f"{querry} gameplay",
        part='snippet',
        type='video',
        maxResults=max_result
    )

    response = request.execute()
    return [
        {
            'title': item['snippet']['title'],
            'video_id': item['id']['videoId'],
        }
        for item in response.get("items", [])
    ]

def search_review(querry,max_result=1):
    youtube = build('youtube','v3',developerKey=YOUTUBE_API_KEY)

    request = youtube.search().list(
        q=f"{querry} review",
        part='snippet',
        type='video',
        maxResults=max_result
    )

    response = request.execute()
    return [
        {
            'title': item['snippet']['title'],
            'video_id': item['id']['videoId'],
        }
        for item in response.get("items", [])
    ]

def search_tips(querry,max_result=1):
    youtube = build('youtube','v3',developerKey=YOUTUBE_API_KEY)

    request = youtube.search().list(
        q=f"{querry} tips",
        part='snippet',
        type='video',
        maxResults=max_result
    )

    response = request.execute()
    return [
        {
            'title': item['snippet']['title'],
            'video_id': item['id']['videoId'],
        }
        for item in response.get("items", [])
    ]