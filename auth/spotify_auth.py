import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def authenticate_user():
    load_dotenv()

    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                # scope="user-library-read, user-top-read, user-read-private",
                                                scope="user-library-read, user-top-read, user-read-private, user-read-recently-played"))
    
    return sp

