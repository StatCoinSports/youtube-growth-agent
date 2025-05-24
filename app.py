import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import Flask, request, jsonify
from google_auth_oauthlib.flow import Flow
from utils.youtube import get_subscribers

app = Flask(__name__)

@app.route('/')
def home():
    return 'YouTube Growth Agent is Live'

@app.route('/stats')
def stats():
    data = get_subscribers()
    return jsonify(data)

@app.route('/authorize')
def authorize():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv("YOUTUBE_CLIENT_ID"),
                "client_secret": os.getenv("YOUTUBE_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [os.getenv("YOUTUBE_REDIRECT_URI")]
            }
        },
        scopes=["https://www.googleapis.com/auth/youtube.readonly"],
        redirect_uri=os.getenv("YOUTUBE_REDIRECT_URI")
    )

    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    return f'<a href="{auth_url}">Click here to log in with YouTube</a>'

@app.route('/oauth2callback')
def oauth2callback():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv("YOUTUBE_CLIENT_ID"),
                "client_secret": os.getenv("YOUTUBE_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [os.getenv("YOUTUBE_REDIRECT_URI")]
            }
        },
        scopes=["https://www.googleapis.com/auth/youtube.readonly"],
        redirect_uri=os.getenv("YOUTUBE_REDIRECT_URI")
    )

    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    refresh_token = credentials.refresh_token

    print("✅ REFRESH TOKEN:", refresh_token)
    return "✅ Success! You’re connected to YouTube. You can close this tab."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

