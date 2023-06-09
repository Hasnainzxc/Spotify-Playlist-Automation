import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify credentials
<<<<<<< HEAD
SPOTIFY_CLIENT_ID = '6e59b1ccce7d4721815e5cc457368afb'
SPOTIFY_CLIENT_SECRET = 'dcfbbf8912f8485294e0b5446ce7a777'
=======
SPOTIFY_CLIENT_ID = 'YOUR ID'
SPOTIFY_CLIENT_SECRET = 'YOUR SECRET KEY'
>>>>>>> c9c2b0145561b341d5c640009670d4f680616209

# YouTube credentials
YOUTUBE_CLIENT_SECRET_FILE = 'YOUR_YOUTUBE_CLIENT_SECRET_FILE.json'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
<<<<<<< HEAD
YOUTUBE_PLAYLIST_ID = 'PLSFYbUMCjMttTG8z8QCEzfEV63IuFa-Yw'
=======
YOUTUBE_PLAYLIST_ID = 'YOUR PLAYLIST ID '
>>>>>>> c9c2b0145561b341d5c640009670d4f680616209

REDIRECT_URI = 'http://localhost:8080/callback'

# Authenticate with Spotify
spotify_credentials = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=spotify_credentials)

# Authenticate with YouTube
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    YOUTUBE_CLIENT_SECRET_FILE, scopes)
flow.redirect_uri = REDIRECT_URI

# Run the local server
credentials = flow.run_local_server(port=8080)

youtube = googleapiclient.discovery.build(
    YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)

# Retrieve your Spotify playlist
def get_spotify_playlist(playlist_id):
    playlist = spotify.playlist(playlist_id, fields='tracks.items(track(name, artists(name)))')
    tracks = playlist['tracks']['items']
    playlist_tracks = []
    for track in tracks:
        name = track['track']['name']
        artists = ', '.join([artist['name'] for artist in track['track']['artists']])
        playlist_tracks.append(f"{name} - {artists}")
    return playlist_tracks

# Retrieve your YouTube playlist
def get_youtube_playlist():
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=YOUTUBE_PLAYLIST_ID,
        maxResults=50  # Increase if your playlist has more than 50 videos
    )
    response = request.execute()
    playlist_items = response['items']
    youtube_playlist = []
    for item in playlist_items:
        video_id = item['snippet']['resourceId']['videoId']
        youtube_playlist.append(video_id)
    return youtube_playlist

# Merge new songs to YouTube playlist
def merge_to_youtube(playlist_tracks):
    youtube_playlist = get_youtube_playlist()
    for track in playlist_tracks:
        search_query = f"{track} audio"
        search_response = youtube.search().list(
            q=search_query,
            part="id",
            maxResults=1
        ).execute()
        search_results = search_response.get('items', [])
        if search_results:
            video_id = search_results[0]['id']['videoId']
            if video_id not in youtube_playlist:
                youtube.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": YOUTUBE_PLAYLIST_ID,
                            "position": 0,
                            "resourceId": {
                                "kind": "youtube#video",
                                "videoId": video_id
                            }
                        }
                    }
                ).execute()
                print(f"Added {track} to YouTube playlist.")
        else:
            print(f"No video found for {track}.")



# Main script
if __name__ == '__main__':
    playlist_id = '7wMhsMpZvfdMk123ItqPEc'
    playlist_tracks = get_spotify_playlist(playlist_id)
    merge_to_youtube(playlist_tracks)

