import pandas as pd
from auth.spotify_auth import authenticate_user


def get_top_tracks(sp, time_range="medium_term", limit=50):

    # fetach top tracks
    results = sp.current_user_top_tracks(time_range=time_range, limit=limit)
    top_tracks = results.get('items', [])

    DATE_FORMAT = "%Y-%m-%d"

    # flattens nested json to dataframe
    df = pd.json_normalize(top_tracks)

    # columns to use
    df = df[[
        "id",
        "name",
        "album.name",
        "album.release_date",
        "duration_ms",
        "popularity",
        "explicit",
        "track_number",
        "artists",
        "external_urls.spotify",
    ]]

    df.rename(columns={
        "id": "track_id",
        "name": "track_name",
        "album.name": "album_name",
        "album.release_date": "album_release_date",
        "external_urls.spotify": "spotify_url",
    }, inplace=True)

    # #create track l"inks to spotify
    # df["spotify_url"] = df["track_id"].apply(lambda tid: f"https://open.spotify.com/track/{tid}")

    #collapse the list of artists into a single comma separated string
    df["artist_names"] = df["artists"].apply(
        lambda artists: ", ".join([artist["name"] for artist in artists]) #for each artist in artists list join the names with a comma
    )

    # convert duration from ms to minutes
    df["duration_min"] = df["duration_ms"] / 60000

    # reorder and drop columns

    df = df[[
        "track_id",
        "track_name",
        "track_number",
        "duration_min",
        "album_name",
        "artist_names",
        "album_release_date",
        "popularity",
        "explicit",
        "spotify_url",
    ]]

    df["album_release_date"] = pd.to_datetime(df["album_release_date"], format=DATE_FORMAT)


    return df




# sp = authenticate_user()
# df = get_top_tracks(sp, time_range="medium_term", limit=3)
# print(df)
if __name__ == "__main__":
    # Quick test/demo
    sp = authenticate_user()
    df = get_top_tracks(sp, time_range="medium_term", limit=10)
    print(df)


#Spotify’s Top Tracks endpoint caps out at 50 per request. If you want top 100, have to page through the results:
# def get_top_tracks(sp, time_range="medium_term", limit=50):
#     items = []
#     offset = 0
#     while offset < limit:
#         batch = sp.current_user_top_tracks(
#             time_range=time_range,
#             limit=min(50, limit - offset),
#             offset=offset
#         )["items"]
#         items.extend(batch)
#         if len(batch) < 50:
#             break
#         offset += 50

#     # then normalize items → DataFrame as before
#     df = pd.json_normalize(items)
#     ...
#     return df