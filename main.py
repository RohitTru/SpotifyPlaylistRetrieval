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
    
        searchResults = VideosSearch(i, limit=1).result().get("result",[])
        if searchResults:
            ytSongURL.append(searchResults[0].get('link'))
        else:
            print(f"no result found for {i}")
    return ytSongURL

def download_From_YT(ytSongURL):
    notFound = 0
    for i in ytSongURL:
        yt = YouTube(i)
    
        try: # Error handling incase of retrieval errors by pytube
            title = yt.title
            filename = title + '.wav'
            yt.streams.get_audio_only().download('wavDownloads', filename)
        except Exception as e:
            print(f"Error retrieving title for video {i}:{str(e)}")
            notFound += 1
    return f"could not find {notFound} out of {len(ytSongURL)}"   
        
        
    
def main():
    token = get_token()
    playlistLink = get_spotify_link()
    playlistId = get_playlistId(playlistLink)
    trackInfo = trackDetails(token, playlistId)
    ytSongURL = get_YT_Link(trackInfo)
    print(download_From_YT(ytSongURL))
    

    
if __name__ == "__main__":
    main()