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
def get_playlistId(playlistLink):

    # retrieve id from link
    playlistId = playlistLink.split('/')[-1].split('?')[0]
    return playlistId

def trackDetails(token, playlistId):
    sp = spotipy.Spotify(auth=token)
     
    playlistTracks = []
    trackInfo = sp.playlist_tracks(playlistId)
    playlistTracks += trackInfo['items']
    while trackInfo['next']:
        trackInfo = sp.next(trackInfo)
        playlistTracks += trackInfo['items']
    
    trackInfo = []
    for track in playlistTracks:
        trackInfo.append(track['track']['name'] + track['track']['artists'][0]['name'] + ' audio')
    return trackInfo

def get_YT_Link(trackInfo):
    ytSongURL = []
    for i in trackInfo:
        search = (VideosSearch(i, limit=1)).result()
        ytSongURL.append(search['result'][0]['link'])
    return ytSongURL

def main():
    token = get_token()
    playlistLink = get_spotify_link()
    playlistId = get_playlistId(playlistLink)
    trackInfo = trackDetails(token, playlistId)
    ytSongURL = get_YT_Link(trackInfo)
    print(ytSongURL)

    
if __name__ == "__main__":
    main()