import pandas as pd
import pprint
from auth.spotify_auth import authenticate_user


def get_top_artists(sp, time_range="medium_term", limit=50):
    """
    Fetch the current user's top artists from Spotify and return a pandas DataFrame.

    Parameters:
        sp: Authenticated spotipy.Spotify client
        time_range (str): One of 'short_term', 'medium_term', or 'long_term'
        limit (int): Number of artists to retrieve (max 50)

    Returns:
        pd.DataFrame: DataFrame containing:
            - artist_id
            - artist_name
            - genres (comma-separated)
            - popularity
            - followers
            - spotify_url
    """

    # FETCH TOP ARTISTS
    results = sp.current_user_top_artists(time_range=time_range, limit=limit)
    top_artists = results.get('items', [])


    # NORMALIZE NESTED JSON TO DATAFRAME
    df = pd.json_normalize(top_artists)

    df = df[[
        "id",
        "name",
        "genres",
        "popularity",
        "followers.total",
        "external_urls.spotify",
    ]]

    # RENAME COLUMNS
    df.rename(columns={
        "id": "artist_id",
        "name": "artist_name",
        "followers.total": "followers",
        "external_urls.spotify": "spotify_url",
    }, inplace=True)

    # COLLAPSE GENRES INTO COMMA-SEPARATED STRING
    df["genres"] = df["genres"].apply(lambda genres: ", ".join(genres))

    #reorder and drop columns
    df = df[[
        "artist_id",
        "artist_name",
        "genres",
        "popularity",
        "followers",
        "spotify_url",
    ]]

    return df
if __name__ == "__main__":

    sp = authenticate_user()
    df = get_top_artists(sp, time_range="medium_term", limit=10)

    pprint.pprint(df)




