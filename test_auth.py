import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="b36873e77f7a4f939a712db4a4df5dff",
                                               client_secret="fda3132b365b41acb5ff67f38047afa1",
                                               redirect_uri="http://127.0.0.1:8888/callback",
                                               scope="user-library-read"))


