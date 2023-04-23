import os
import spotipy
import spotipy.util as util
import sys
import base64
import json
from dotenv import load_dotenv
from youtubesearchpython import VideosSearch
from pytube import YouTube
from requests import post

# load secrets
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Spotify authorization token function
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
            }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# Anytime we make api calls
def get_auth_header(token):
    return{"Authorization": "Bearer " + token}

# Retrieves the spotify playlist from user
def get_spotify_link():
        playlistLink = input("Please enter a spotify playlist link: ")
        return playlistLink
        

# Extracts the spotify playlist ID from playlist link.
def get_playlistId(token, playlistLink):
    # giving access to spotipy
    sp = spotipy.Spotify(auth=token)
       
    # retrieve id from link
    playlistId = playlistLink.split('/')[-1].split('?')[0]
    return playlistId



token = get_token()

print(get_playlistId(token, get_spotify_link()))

