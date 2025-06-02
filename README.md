## SpotifyUwrapped

A Python-based ETL pipeline to extract, transform, and analyze your Spotify user data using only supported Web API endpoints. Designed to work without deprecated features (e.g., audio-features, recommendations) which now require extended access.

## Features

- Authentication via OAuth2 (user-top-read, user-read-private, user-read-recently-played, user-library-read)
- Ingests top tracks, artists, recently played tracks, saved tracks, playlists, and artist genres
- Transforms data into clean pandas DataFrames
- Provides summary metrics such as total listening time, plays per day, genre distribution, and top tracks/artists
- Exports all tables to CSV for further analysis

## Prerequisites

- Python 3.8+
- A Spotify Developer account and app (created before Nov 27, 2024, or with extended access)
- Environment variables in a `.env` file:

  ```ini
  SPOTIPY_CLIENT_ID=your_client_id
  SPOTIPY_CLIENT_SECRET=your_client_secret
  SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
  ```

## Installation

```bash
git clone https://github.com/yourusername/custom-spotify-wrapped.git
cd custom-spotify-wrapped
python -m venv venv
source venv/bin/activate   # on macOS/Linux
# venv\Scripts\activate  # on Windows
pip install -r requirements.txt
```

## Limitations

- Audio Features, Recommendations, and Related Artists endpoints require Spotify extended access and are not supported by default.
- Data is limited to the top 50 or recently played 50 items per endpoint unless extended pagination is implemented.

## Future Work

- Add Matplotlib/Streamlit visualizations
- Package as CLI tool or Docker container
- Schedule regular runs with cron or GitHub Actions
- Expand pagination to fetch full history

## Next Steps

- Integrate Gemini-based roast generator.
- Add image collage feature from album art.
- Decide between Discord bot and web frontend.
