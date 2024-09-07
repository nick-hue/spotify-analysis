import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from datetime import datetime
import json

load_dotenv()

class TrackInfo:
    def __init__(self, id, track_name, artists, added_at, added_by, duration_ms) -> None:
        self.id = id
        self.track_name = track_name
        self.artists = [artist['name'] for artist in artists]
        self.added_at = datetime.strptime(added_at, "%Y-%m-%dT%H:%M:%SZ").strftime("%m-%d-%Y")
        self.added_by = sp.user(added_by['id'])['display_name']
        self.duration_ms = duration_ms

        
    def display(self):
        print(f"{self.track_name} - {", ".join(self.artists)} - Added by : {self.added_by} at {self.added_at}")

    def to_dict(self):
        return {
            'id': self.id,
            'track_name': self.track_name,
            'artists': self.artists,
            'added_at': self.added_at,  
            'added_by': self.added_by,
            'duration_ms': self.duration_ms
        }

# Retrieve Spotify credentials from environment variables
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
playlist_id = os.getenv('SPOTIFY_PLAYLIST_ID')
print(playlist_id)
# Initialize Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="playlist-read-private"))

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

final_tracks = [TrackInfo(idx, track['track']['name'], track['track']['artists'], track['added_at'], track['added_by'], track['track']['duration_ms']) for idx, track in enumerate(tracks)]

track_info_dicts = [track_info.to_dict() for track_info in final_tracks]

# Save the list of dictionaries to a JSON file
with open('tracks.json', 'w', encoding='utf-8') as json_file:
    json.dump(track_info_dicts, json_file, ensure_ascii=False, indent=4)

print("Track info has been saved to tracks.json")

