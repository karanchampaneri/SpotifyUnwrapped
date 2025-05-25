import pandas as pd
from auth.spotify_auth import authenticate_user

def get_artists_genres(sp, artist_ids):
    """
    Given a Spotipy client and a list of artist IDs,
    fetch each artist's genres and return a DataFrame with:
        - artist_id
        - genres (comma-separated string)
    """

    all_artists = []

    # SPOTIFY API LIMITS TO 50 ARTISTS PER REQUEST (per batch)
    for i in range(0, len(artist_ids), 50):
        batch = artist_ids[i : i + 50]
        response = sp.artists(batch)
        all_artists.extend(response.get('artists', []))

    # NORMALIZE NESTED JSON TO DATAFRAME
    df = pd.json_normalize(all_artists)[['id', 'genres']]
    df.rename(columns={
        "id": "artist_id",
    }, inplace=True)

    # COLLAPSE GENRES INTO COMMA-SEPARATED STRING OR EMPTY STRING
    df["genres"] = df["genres"].apply(lambda genres: ", ".join(genres) if isinstance(genres, list) else "")

    return df


if __name__ == '__main__':
    #smoke test
    sp = authenticate_user()
    from ingest.top_artists import get_top_artists


    # FETCH TOP ARTISTS
    top_artists_df = get_top_artists(sp, limit=10)
    artist_ids = top_artists_df["artist_id"].to_list()

    # FETCH GENRES FOR EACH ARTIST
    genres_df = get_artists_genres(sp, artist_ids)
    print(f"\n-------- ARTIST IDS --------")
    print(artist_ids)
    print(f"\n-------- GENRES --------")
    print(genres_df)









