import pandas as pd
from auth.spotify_auth import authenticate_user

def get_genres(sp):
    """
    Fetch the current user's genres from Spotify and return a pandas DataFrame.

    Parameters:
        sp: Authenticated spotipy.Spotify client

    Returns:
        pd.DataFrame: DataFrame containing:
            - genre_id
            - genre_name
            - genre_description
            - spotify_url
    """

    

