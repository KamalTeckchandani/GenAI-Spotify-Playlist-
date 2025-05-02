# --- spotify_utils.py (Updated for Artist ID Flow) ---

import os
import spotipy
import requests
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# --- Load environment variables ---
load_dotenv()

# --- Setup Spotify Client ---
def get_spotify_client():
    auth_manager = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-public"
    )

    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=3)
    session.mount('https://', adapter)

    sp = spotipy.Spotify(auth_manager=auth_manager, requests_session=session)
    return sp

# --- Fetch Candidate Songs ---
def fetch_candidate_songs(sp, artist_ids, artist_names, genres, date_range):
    candidate_songs = set()
    start_year, end_year = 0, 3000

    # Parse date range
    if date_range:
        try:
            parts = date_range.split('-')
            if len(parts) == 2:
                start_year, end_year = int(parts[0]), int(parts[1])
        except Exception:
            pass

    # --- Fetch Songs by Artist IDs ---
    if artist_ids:
        for idx, artist_id in enumerate(artist_ids):
            artist_name = artist_names[idx] if idx < len(artist_names) else "Unknown Artist"
            try:
                albums = sp.artist_albums(artist_id, album_type='album', limit=50)['items']
                album_ids = list(set([album['id'] for album in albums]))

                for album_id in album_ids:
                    album_info = sp.album(album_id)
                    release_date = album_info.get('release_date', '1900')
                    release_year = release_date[:4]

                    if release_year.isdigit() and start_year <= int(release_year) <= end_year:
                        album_tracks = album_info['tracks']['items']
                        for track in album_tracks:
                            song_title = track['name']
                            candidate_songs.add(f"{song_title} - {artist_name}")

            except Exception as e:
                print(f"❌ Error fetching tracks for artist ID {artist_id}: {e}")
                continue

    # --- Genre fallback if no artists ---
    if not artist_ids and genres:
        for genre in genres:
            try:
                genre_tracks = sp.search(q=f'genre:"{genre}"', type='track', limit=50)
                for track in genre_tracks['tracks']['items']:
                    release_date = track['album'].get('release_date', '1900')
                    release_year = release_date[:4]
                    if release_year.isdigit() and start_year <= int(release_year) <= end_year:
                        song_artist = track['artists'][0]['name']
                        song_title = track['name']
                        candidate_songs.add(f"{song_title} - {song_artist}")
            except Exception as e:
                print(f"Error fetching genre {genre}: {e}")
                continue

    return list(candidate_songs)
