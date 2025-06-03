import pandas as pd
from auth.spotify_auth import authenticate_user

def get_saved_tracks(sp, limit=50):

    """
    Fetch the current user's saved (liked) tracks from Spotify and return a pandas DataFrame.

    Parameters:
        sp: Authenticated spotipy.Spotify client
        limit (int): Number of saved tracks to retrieve (max 50)

    Returns:
        pd.DataFrame: DataFrame containing:
            - added_at (datetime user saved the track)
            - track_id
            - track_name
            - artist_names
            - album_name
            - album_release_date (datetime)
            - duration_min
            - popularity
            - explicit
            - spotify_url
    """

    # FETCH SAVED TRACKS
    results = sp.current_user_saved_tracks(limit=limit)
    items = results.get('items', [])

    df = pd.json_normalize(items)

    # SELECT RELEVENT COLUMNS
    df = df[[
        "added_at",
        "track.id",
        "track.name",
        "track.artists",
        "track.album.name",
        "track.album.release_date",
        "track.duration_ms",
        "track.popularity",
        "track.explicit",
        "track.external_urls.spotify"
    ]]
    
    df.rename(columns={
        "track.id": "track_id",
        "track.name": "track_name",
        "track.album.name": "album_name",
        "track.album.release_date": "album_release_date",
        "track.duration_ms": "duration_ms",
        "track.popularity": "popularity",
        "track.explicit": "explicit",
        "track.external_urls.spotify": "spotify_url",
    }, inplace=True)

    # Flatten artists list of dicts to a comma-separated string
    df["artist_names"] = df["track.artists"].apply(
        lambda artists: ", ".join([artist["name"] for artist in artists]) #for each artist in artists list join the names with a comma
    )

    # Convert duration from ms to minutes
    df["duration_min"] = df["duration_ms"] / 60000

    # PARSE DATE FIELDS

    df["added_at"] = pd.to_datetime(df["added_at"], utc=True)
    df["album_release_date"] = pd.to_datetime(df["album_release_date"], errors="coerce")

    # REORDER AND DROP COLUMNS
    df = df[[
        "track_id",
        "track_name",
        "added_at",
        "artist_names",
        "album_name",
        "album_release_date",
        "duration_min",
        "popularity",
        "explicit",
        "spotify_url",
    ]]

    return df



if __name__ == '__main__':
    #smoke test
    sp = authenticate_user()
    df = get_saved_tracks(sp, limit=20)
    print(df)