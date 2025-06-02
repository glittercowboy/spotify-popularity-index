# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Spotify Artist Popularity Index - A Flask web application that displays Spotify artists' popularity scores and their latest releases through a clean, dark-themed interface.

## Architecture

The project has dual entry points for local and Vercel deployment:
- `app.py` - Local development server (port 5001)
- `api/index.py` - Vercel serverless function (identical functionality, adjusted paths)

Both files contain duplicate logic with minor differences:
- `api/index.py` uses `template_folder='../templates'` for Vercel's file structure
- `api/index.py` includes additional logging for debugging in production

## Key Functionality

1. **Artist Search**: Real-time search with dropdown showing artist results, popularity scores, and follower counts
2. **Artist Popularity Display**: Shows artist name, image, and popularity score (0-100)
3. **Latest Release Tracking**: Fetches and displays the most recent album/single with its own popularity score
4. **Full Discography**: Displays releases in a paginated grid (10 at a time) with "Load More" functionality
5. **Error Handling**: Graceful handling of missing credentials and invalid artist IDs

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run local development server
python app.py
# Server runs at http://localhost:5001/<artist_id>
```

## Environment Configuration

Required environment variables in `.env`:
```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```

## Deployment

Deployed to Vercel using `vercel.json` configuration. All routes are handled by `api/index.py` as a serverless function.

## Important Implementation Details

- Uses Spotify Web API via `spotipy` library to fetch artist and album data
- `get_latest_release()` function sorts up to 50 albums/singles by release date to find the most recent
- `get_discography()` function provides paginated album/single data with full popularity scores
- `/api/search` endpoint provides artist search with results sorted by popularity
- `/api/discography/<artist_id>` endpoint handles AJAX requests for progressive loading
- Search functionality includes 300ms debouncing to prevent excessive API calls
- Catch-all route pattern allows artist IDs directly in URL path (e.g., `/0xD1RASjJGXnTh5NxdrKxF`)
- Templates use Spotify's dark theme colors (#121212 background, #1DB954 accent)
- No test suite or linting configuration currently exists