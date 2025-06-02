from flask import Flask, render_template, request
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

def get_discography(artist_id, offset=0, limit=10):
    try:
        # Get the artist's albums with pagination
        albums = sp.artist_albums(artist_id, album_type='album,single', limit=limit, offset=offset)
        
        if not albums or not albums['items']:
            return {'releases': [], 'total': 0, 'has_more': False}
        
        # Get full details for each album to include popularity
        releases = []
        for album in albums['items']:
            try:
                album_full = sp.album(album['id'])
                releases.append({
                    'id': album['id'],
                    'name': album['name'],
                    'release_date': album['release_date'],
                    'popularity': album_full['popularity'],
                    'album_type': album['album_type'].title(),
                    'total_tracks': album['total_tracks'],
                    'image_url': album['images'][0]['url'] if album['images'] else None,
                    'url': album['external_urls']['spotify'] if 'external_urls' in album else None
                })
            except Exception as e:
                print(f"Error getting album details for {album['id']}: {str(e)}")
                continue
        
        # Sort by release date (newest first)
        releases.sort(key=lambda x: x['release_date'], reverse=True)
        
        return {
            'releases': releases,
            'total': albums['total'],
            'has_more': offset + limit < albums['total']
        }
    except Exception as e:
        print(f"Error getting discography: {str(e)}")
        return {'releases': [], 'total': 0, 'has_more': False}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    try:
        if not path:
            return render_template('home.html')
        
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
        
        # Get initial discography (first 50 releases)
        discography = get_discography(path, offset=0, limit=50)
        
        return render_template('index.html', 
                             artist_name=artist['name'],
                             artist_id=path,
                             popularity=artist['popularity'],
                             image_url=artist['images'][0]['url'] if artist['images'] else None,
                             latest_release=latest_release,
                             discography=discography)
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return render_template('error.html', 
                             error="Invalid artist ID or API error. Please check your Spotify artist ID.")

@app.route('/api/discography/<artist_id>')
def get_more_releases(artist_id):
    try:
        if not sp:
            return {'error': 'Spotify API not configured'}, 500
        
        # Get offset from query parameters
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 50))
        
        # Get discography with pagination
        discography = get_discography(artist_id, offset=offset, limit=limit)
        
        return discography
    except Exception as e:
        print(f"Error getting more releases: {str(e)}")
        return {'error': 'Failed to load releases'}, 500

@app.route('/api/search')
def search_artists():
    try:
        if not sp:
            return {'error': 'Spotify API not configured'}, 500
        
        # Get search query
        query = request.args.get('q', '').strip()
        if not query:
            return {'artists': []}
        
        # Search for artists
        results = sp.search(q=query, type='artist', limit=10)
        
        artists = []
        for artist in results['artists']['items']:
            artists.append({
                'id': artist['id'],
                'name': artist['name'],
                'popularity': artist['popularity'],
                'image_url': artist['images'][0]['url'] if artist['images'] else None,
                'followers': artist['followers']['total']
            })
        
        # Sort by popularity
        artists.sort(key=lambda x: x['popularity'], reverse=True)
        
        return {'artists': artists}
    except Exception as e:
        print(f"Error searching artists: {str(e)}")
        return {'error': 'Failed to search artists'}, 500

# For local development
if __name__ == '__main__':
    app.run(debug=True, port=5001)
