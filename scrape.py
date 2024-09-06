import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv(override=True)

# Retrieve Spotify credentials from environment variables
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
print(redirect_uri)
# Initialize Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="playlist-read-private"))

# Playlist ID or URL (You can use either ID or full playlist URL)
playlist_id = "https://open.spotify.com/playlist/1WqnEOujkN0ruzIubwAO5s?si=25112cb6edc54204"
# Get information for the specific playlist
playlist_info = sp.playlist(playlist_id)

tracks = []
results = sp.playlist_tracks(playlist_id, offset=0)

while results:
    tracks.extend(results['items'])
    if results['next']:
        results = sp.next(results)  # Fetch the next page of results
    else:
        results = None

# Print track details
for idx, track in enumerate(tracks):
    track_info = track['track']
    print(f"{idx + 1}. {track_info['name']} - {track_info['artists'][0]['name']}")