import os
import spotipy
import spotipy.util as util
import sys
from dotenv import load_dotenv
from youtubesearchpython import VideosSearch
from pytube import YouTube

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

