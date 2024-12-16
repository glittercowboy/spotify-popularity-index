from flask import Flask, render_template
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='../templates')

# Initialize Spotify client
try:
    client_credentials_manager = SpotifyClientCredentials(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
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
            return render_template('error.html', 
                                error="Spotify API configuration error. Please check the server configuration.")
        
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
