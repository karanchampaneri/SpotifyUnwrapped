import pandas as pd
from auth.spotify_auth import authenticate_user

def get_recently_played(sp, limit=50):
    """
    Fetch the current user's recently played tracks from Spotify and return a pandas DataFrame.

    Parameters:
        sp: Authenticated spotipy.Spotify client
        limit (int): Number of recent tracks to retrieve (max 50)

    Returns:
        pd.DataFrame: DataFrame containing:
            - played_at (datetime)
            - track_id
            - track_name
            - artist_names
            - album_name
            - album_release_date (datetime)
            - duration_min
            - context (e.g., playlist/album URI)
            - spotify_url
    """
    # FETCH RECENTLY PLAYED TRACKS
    results = sp.current_user_recently_played(limit=limit)
    items = results.get('items', [])

    # NORMALIZE NESTED JSON TO DATAFRAME
    df = pd.json_normalize(items)

    df = df[[
        "played_at",
        "track.id",
        "track.name",
        "track.artists",
        "track.album.name",
        "track.album.release_date",
        "track.duration_ms",
        "context.uri",
        "track.external_urls.spotify",
    ]]

    df.rename(columns={
        "track.id": "track_id",
        "track.name": "track_name",
        "track.album.name": "album_name",
        "track.album.release_date": "album_release_date",
        "track.duration_ms": "duration_ms",
        "context.uri": "context_uri",
        "track.external_urls.spotify": "spotify_url",
    }, inplace=True)
    
    # Flatten artists list of dicts to a comma-separated string
    df["artist_names"] = df["track.artists"].apply(
        lambda artists: ", ".join([artist["name"] for artist in artists]) #for each artist in artists list join the names with a comma
    )

    # Convert duration from ms to minutes
    df["duration_min"] = df["duration_ms"] / 60000

    # Date Fields
    DATE_FORMAT = "%Y-%m-%d"
    df["played_at"] = pd.to_datetime(df["played_at"], utc=True)
    df["album_release_date"] = pd.to_datetime(df["album_release_date"], errors="coerce")
    
    df = df[[
        "played_at",
        "track_id",
        "track_name",
        "artist_names",
        "album_name",
        "album_release_date",
        "duration_min",
        "context_uri",
        "spotify_url",
    ]]

    return df

if __name__ == '__main__':
    #smoke test
    sp = authenticate_user()
    df = get_recently_played(sp, limit=20)
    print(df)