import spotipy
import pandas as pd

from auth.spotify_auth import authenticate_user

sp = authenticate_user()

# Get top 

def get_top_tracks(sp, time_range="medium_term", limit=50):

    # fetach top tracks
    results = sp.current_user_top_tracks(time_range=time_range, limit=limit)
    # print(results, type(results))
    top_tracks = results['items']

    # flattens nested json in list of dicts to df
    df = pd.json_normalize(top_tracks)

    # columns to use
    df = df[[
        "name",
        "album.name",
        "duration_ms",
        "popularity",
        "id",
        "artists"
    ]]

    df.rename(columns={
        "name": "track_name",
        "album.name": "album_name",
        "id": "track_id",
    }, inplace=True)

    #

    print(df)

get_top_tracks(sp, 'medium_term', 3 )