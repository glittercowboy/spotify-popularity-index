# Spotify Artist Popularity Index

A simple web interface that displays a Spotify artist's popularity index. This tool allows artists to monitor their Spotify popularity score through a clean, modern interface.

## Setup

1. Clone the repository
```bash
git clone https://github.com/glittercowboy/spotify-popularity-index.git
cd spotify-popularity-index
```

2. Create a virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file with your Spotify API credentials:
```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```

4. Run the application
```bash
python app.py
```

5. Access the application at:
```
http://localhost:5001/<artist_id>
```
Replace `<artist_id>` with the Spotify artist ID you want to check.

## Finding Your Spotify Artist ID

You can find your Spotify artist ID by:
1. Going to your Spotify artist profile
2. Clicking "Share"
3. Selecting "Copy Spotify URI"
4. The ID is the string after "spotify:artist:"

Example: For the URI `spotify:artist:0xD1RASjJGXnTh5NxdrKxF`, the artist ID is `0xD1RASjJGXnTh5NxdrKxF`
