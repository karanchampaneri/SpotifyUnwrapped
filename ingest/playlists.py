import pandas as pd
from auth.spotify_auth import authenticate_user

def get_user_playlists(sp, limit=50):
    
    results = sp.current_user_playlists(limit=limit)
    playlists = results.get('items', [])

    while results.get('next'):
        results = sp.next(results)
        playlists.extend(results.get('items', []))
    
    # NORMALIZE NESTED JSON TO DATAFRAME
    df = pd.json_normalize(playlists)

    # SELECT RELEVENT COLUMNS
    df = df[[
        "id",
        "name",
        "owner.display_name",
        "tracks.total",
        "external_urls.spotify",
    ]]

    df.rename(columns={
        "id": "playlist_id",
        "name": "playlist_name",
        "owner.display_name": "playlist_owner",
        "tracks.total": "playlist_tracks",
        "external_urls.spotify": "spotify_url",
        }, inplace=True)
    
    return df


def get_playlist_tracks(sp, playlist_id, limit=50):

    # FETCH PLAYLIST ITEMS and handle pagination

    results = sp.playlist_items(playlist_id)
    items = results.get('items', [])

    while results.get('next'):
        results = sp.next(results)
        items.extend(results.get('items', []))

    # NORMALIZE NESTED JSON TO DATAFRAME
    df = pd.json_normalize(items)

    # SELECT RELEVENT COLUMNS
    df = df[[
        "track.id",
        "track.name",
        "track.artists",
        "track.album.name",
        "added_at",
        "track.uri", ## TODO: check if this is the same as track.external_urls.spotify
    ]] 

    df.rename(columns={
        "track.id": "track_id",
        "track.name": "track_name",
        "track.artists": "artist_names",
        "track.album.name": "album_name",
        "added_at": "added_at",
        "track.uri": "spotify_url"
    }, inplace=True)

    # Flatten artists list of dicts to a comma-separated string
    df["artist_names"] = df["artist_names"].apply(
        lambda artists: ", ".join([artist["name"] for artist in artists]) #for each artist in artists list join the names with a comma
    )

    # PARSE DATE FIELDS and attach Playlist ID

    df["added_at"] = pd.to_datetime(df["added_at"], utc=True)
    df["playlist_id"] = playlist_id

    # REORDER AND DROP COLUMNS
    df = df[[
        "playlist_id",
        "track_id",
        "track_name",
        "artist_names",
        "album_name",
        "added_at",
        "spotify_url",
        ]]
    
    return df



if __name__ == '__main__':
    #smoke test
    sp = authenticate_user()
    playlists_df = get_user_playlists(sp, limit=20)
    print(playlists_df)

    if not playlists_df.empty:
        playlist_id = playlists_df.iloc[0]["playlist_id"]
        tracks_df = get_playlist_tracks(sp, playlist_id, limit=20)
        print(f"\n-------- {playlists_df.iloc[0]["playlist_name"]} TRACKS --------")
        print(tracks_df.head())