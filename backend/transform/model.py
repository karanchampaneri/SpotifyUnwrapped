import pandas as pd
from ingest.top_tracks import get_top_tracks
from ingest.top_artists import get_top_artists
from ingest.recently_played import get_recently_played
from ingest.saved_tracks import get_saved_tracks
from ingest.playlists import get_user_playlists, get_playlist_tracks

def build_model(sp, limit=50):
    """
    Fetch all source DataFrames and return a dict of modeled tables:
      {
        'tracks': <tracks_df>,
        'artists': <artists_df>,
        'plays': <plays_df>,
        'saved': <saved_df>,
        'playlists': <playlists_df>,
        'playlist_tracks': <playlist_tracks_df>,
      }
    """

    #1. Pull in each DataFrame

    tracks_df = get_top_tracks(sp, limit=limit)
    artists_df = get_top_artists(sp, limit=limit)
    plays_df = get_recently_played(sp, limit=limit)
    saved_df = get_saved_tracks(sp, limit=limit)
    playlists_df = get_user_playlists(sp, limit=limit)

    #2. For each playlist, accumulate tracks into a single DataFrame

    playlist_tracks_df = []
    for pid in playlists_df["playlist_id"]:
        df_pt = get_playlist_tracks(sp, pid)
        playlist_tracks_df.append(df_pt)
    if playlist_tracks_df:
        playlist_tracks_df = pd.concat(playlist_tracks_df, ignore_index=True)
    else:
        playlist_tracks_df = pd.DataFrame(columns=[
            "playlist_id",
            "track_id",
            "track_name",
            "artist_names",
            "album_name",
            "added_at",
            "spotify_url",
        ])

    # 3. Return a dict of clean tables (dataframes)
    return {
        "tracks": tracks_df,
        "artists": artists_df,
        "recent_plays": plays_df,
        "saved": saved_df,
        "playlists": playlists_df,
        "playlist_tracks": playlist_tracks_df,
    }

if __name__ == '__main__':
    #smoke test
    from auth.spotify_auth import authenticate_user
    sp = authenticate_user()
    model = build_model(sp, limit=20)

    for name, df in model.items():
        print(f"\n-------- {name.upper()} --------")
        print(df.shape)

