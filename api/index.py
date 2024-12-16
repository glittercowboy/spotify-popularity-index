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
        
        return render_template('index.html', 
                             artist_name=artist['name'],
                             popularity=artist['popularity'],
                             image_url=artist['images'][0]['url'] if artist['images'] else None)
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return render_template('error.html', 
                             error="Invalid artist ID or API error. Please check your Spotify artist ID.")

# For local development
if __name__ == '__main__':
    app.run(debug=True, port=5001)
