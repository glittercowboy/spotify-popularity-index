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
http://localhost:5001
```

## Using the Application

1. **Search for Artists**: Simply type an artist's name in the search bar
2. **View Artist Stats**: Click on any artist from the search results to see:
   - Current popularity score (0-100)
   - Latest release information
   - Full discography with popularity scores for each release
3. **Direct Access**: You can also directly navigate to an artist using their Spotify ID:
   ```
   http://localhost:5001/<artist_id>
   ```
