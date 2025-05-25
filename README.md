## SpotifyUwrapped

A Python-based ETL pipeline to extract, transform, and analyze your Spotify user data using only supported Web API endpoints. Designed to work without deprecated features (e.g., audio-features, recommendations) which now require extended access.

## 🚀 Features

- **Authentication** via OAuth2 (user-top-read, user-read-private, user-read-recently-played, user-library-read)
- **Ingestion** of:

  - Top Tracks & Top Artists
  - Recently Played Tracks
  - Saved (Liked) Tracks
  - User Playlists & Playlist Tracks
  - Artist Genres

- **Transformation** into clean pandas DataFrames
- **Summary Metrics**:

  - Total listening time
  - Plays per day
  - Genre distribution among top artists
  - Top tracks by popularity
  - Top artists by follower count

- **Export** all tables to CSV for further analysis

## 📋 Prerequisites

- Python 3.8+
- A Spotify Developer account and app (created before Nov 27, 2024, or with extended access)
- Environment variables in a `.env` file:

  ```ini
  SPOTIPY_CLIENT_ID=your_client_id
  SPOTIPY_CLIENT_SECRET=your_client_secret
  SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
  ```

## ⚙️ Installation

```bash
git clone https://github.com/yourusername/custom-spotify-wrapped.git
cd custom-spotify-wrapped
python -m venv venv
source venv/bin/activate   # on macOS/Linux
# venv\Scripts\activate  # on Windows
pip install -r requirements.txt
```

## 📂 Project Structure

```
custom-spotify-wrapped/
├── .env                # your Spotify credentials
├── .gitignore
├── requirements.txt
├── README.md
├── auth/               # OAuth2 authentication
│   └── spotify_auth.py
├── ingest/             # data ingestion modules
│   ├── top_tracks.py
│   ├── top_artists.py
│   ├── recently_played.py
│   ├── saved_tracks.py
│   ├── playlists.py
│   └── genres.py
├── transform/          # build relational tables
│   └── model.py
├── summarize/          # summary metric functions
│   └── metrics.py
├── output/             # CSV export utility
│   └── export.py
├── data/               # generated CSV output
└── main.py             # orchestrates the full ETL & analysis
```

## ⚠️ Limitations

- **Audio Features**, **Recommendations**, **Related Artists** endpoints require Spotify extended access and are not supported by default.
- Data is limited to the top 50 or recently played 50 items per endpoint unless extended pagination is implemented.

## 🌟 Future Work

- Add Matplotlib/Streamlit visualizations
- Package as CLI tool or Docker container
- Schedule regular runs with cron or GitHub Actions
- Expand pagination to fetch full history
