from flask import Flask, render_template
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='../templates')

# Get credentials
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Initialize Spotify client
try:
    if not client_id or not client_secret:
        print(f"Missing credentials - ID: {'Present' if client_id else 'Missing'}, Secret: {'Present' if client_secret else 'Missing'}")
        sp = None
    else:
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        print("Successfully initialized Spotify client")
except Exception as e:
    print(f"Error initializing Spotify client: {str(e)}")
    sp = None

def get_latest_release(artist_id):
    try:
        # Get the artist's albums
        albums = sp.artist_albums(artist_id, album_type='album,single', limit=50)
        
        if not albums or not albums['items']:
            return None
        
        # Sort by release date and get the most recent
        latest_release = max(albums['items'], key=lambda x: x['release_date'])
        
        # Get full album details to get popularity
        latest_release_full = sp.album(latest_release['id'])
        
        return {
            'name': latest_release['name'],
            'release_date': latest_release['release_date'],
            'popularity': latest_release_full['popularity'],
            'image_url': latest_release['images'][0]['url'] if latest_release['images'] else None,
            'url': latest_release['external_urls']['spotify'] if 'external_urls' in latest_release else None
        }
    except Exception as e:
        print(f"Error getting latest release: {str(e)}")
        return None

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    try:
        if not path:
            return render_template('error.html', 
                                error="Please provide a Spotify artist ID in the URL (e.g., /0xD1RASjJGXnTh5NxdrKxF)")
        
        if not sp:
            error_msg = "Spotify API configuration error. "
            if not client_id or not client_secret:
                error_msg += "Missing API credentials. "
            error_msg += "Please check the server configuration."
            return render_template('error.html', error=error_msg)
        
        # Get artist info
        artist = sp.artist(path)
        
        # Get latest release info
        latest_release = get_latest_release(path)
        
        return render_template('index.html', 
                             artist_name=artist['name'],
                             popularity=artist['popularity'],
                             image_url=artist['images'][0]['url'] if artist['images'] else None,
                             latest_release=latest_release)
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return render_template('error.html', 
                             error="Invalid artist ID or API error. Please check your Spotify artist ID.")

# For local development
if __name__ == '__main__':
    app.run(debug=True, port=5001)
