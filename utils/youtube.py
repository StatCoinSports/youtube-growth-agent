import os
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_subscribers():
    creds = Credentials(
        None,
        refresh_token=os.getenv("YOUTUBE_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("YOUTUBE_CLIENT_ID"),
        client_secret=os.getenv("YOUTUBE_CLIENT_SECRET")
    )

    creds.refresh(google.auth.transport.requests.Request())
    service = build("youtube", "v3", credentials=creds)
    request = service.channels().list(part="statistics", mine=True)
    response = request.execute()
    stats = response['items'][0]['statistics']

    return {
        "subscribers": stats['subscriberCount'],
        "views": stats['viewCount'],
        "videos": stats['videoCount']
    }