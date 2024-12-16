from flask import Flask, render_template
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='../templates')

# Initialize Spotify client
client_credentials_manager = SpotifyClientCredentials(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

@app.route('/')
def home():
    return render_template('error.html', 
                         error="Please provide a Spotify artist ID in the URL (e.g., /0xD1RASjJGXnTh5NxdrKxF)")

@app.route('/<artist_id>')
def index(artist_id):
    try:
        # Get artist info
        artist = sp.artist(artist_id)
        
        return render_template('index.html', 
                             artist_name=artist['name'],
                             popularity=artist['popularity'],
                             image_url=artist['images'][0]['url'] if artist['images'] else None)
    except Exception as e:
        return render_template('error.html', 
                             error="Invalid artist ID or API error. Please check your Spotify artist ID.")

# For local development
if __name__ == '__main__':
    app.run(debug=True, port=5001)
