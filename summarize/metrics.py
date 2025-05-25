# summarize/metrics.py
import pandas as pd

def total_listening_time(plays_df):
    #Compute total listening time in minutes from the plays DataFrame.
    total_listening_time = plays_df["duration_min"].sum()    
    return total_listening_time

def plays_per_day(plays_df):
    #Compute the number of plays per day from the plays DataFrame.

    df = plays_df.copy()
    df["date"] = df["played_at"].dt.date
    df = df.groupby("date").size().reset_index(name="plays_per_day")
    return df
    # pass

def top_genres(artists_df):
    #Compute the top genres from the artists DataFrame.
    exploded = artists_df.assign(
        genre=artists_df["genres"].str.split(", ")
    ).explode("genre")

    return exploded['genre'].value_counts()

def top_tracks(tracks_df, n=10):
    #Compute the top n tracks from the tracks DataFrame.
    return tracks_df.sort_values('popularity', ascending=False).head(n)

def top_artists_by_followers(artists_df, n=10):
    #Compute the top n artists by followers from the artists DataFrame.
    return artists_df.sort_values('followers', ascending=False).head(n)


if __name__ == '__main__':
    #quick smoke test

    from auth.spotify_auth import authenticate_user
    from transform.model import build_model
    sp = authenticate_user()
    model = build_model(sp, limit=20)
    plays_df = model["recent_plays"]
    artists_df = model["artists"]

    print("Total listening time (min):", total_listening_time(plays_df))
    print("Plays per day:\n", plays_per_day(plays_df))
    print("Top genres:\n", top_genres(artists_df).head(10))
    print("Top tracks by popularity:\n", top_tracks(model["tracks"], n=5))
    print("Top artists by followers:\n", top_artists_by_followers(artists_df, n=5))