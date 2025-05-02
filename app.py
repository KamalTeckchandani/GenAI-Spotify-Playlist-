import streamlit as st
import re
from spotify_utils import get_spotify_client, fetch_candidate_songs
from genai_utils import generate_playlist_name, generate_playlist_songs

# --- Spotify client ---
sp = get_spotify_client()

st.title("🎵 GenAI Custom Playlist Creator")

# --- Initialize session states ---
if "selected_artists" not in st.session_state:
    st.session_state.selected_artists = []
if "artist_id_mapping" not in st.session_state:
    st.session_state.artist_id_mapping = {}

# --- Artist Search Section ---
st.subheader("🔎 Search and Select Artist(s) (Live from Spotify)")

artist_search_input = st.text_input("Start typing an artist name:")

new_artist_results = []
artist_id_mapping_temp = {}

if artist_search_input:
    with st.spinner("🔎 Searching Spotify..."):
        search_results = sp.search(q=f'artist:{artist_search_input}', type='artist', limit=10)

        if search_results['artists']['items']:
            for artist in search_results['artists']['items']:
                name = artist['name']
                artist_id = artist['id']
                new_artist_results.append((name, artist_id))

    # --- Sort search results: Exact match > partial match > others ---


    # Update mapping only for newly found artists
    for artist_name, artist_id in new_artist_results:
        if artist_name not in st.session_state.artist_id_mapping:
            st.session_state.artist_id_mapping[artist_name] = artist_id

# --- Build Artist Options ---
already_selected = st.session_state.selected_artists
newly_searched = [artist_name for artist_name, _ in new_artist_results]

# Merge selections carefully (no duplicates)
all_available_artists = list(dict.fromkeys(already_selected + newly_searched))
all_available_artists = sorted(
    all_available_artists,
    key=lambda x: (
        0 if x.lower() == artist_search_input.strip().lower() else
        1 if artist_search_input.strip().lower() in x.lower() else
        2
    )
)
# --- Artist Multi-select ---
selected_now = st.multiselect(
    "Pick Artist(s):",
    options=all_available_artists,
    default=already_selected,
    help="Pick multiple artists. Previous selections remain."
)

# Update selected artists
st.session_state.selected_artists = selected_now

# --- Playlist Settings ---
genre_choices = [
    "pop", "rock", "hip hop", "indie", "electronic", "rap", "country", "metal", "jazz",
    "classical", "blues", "reggae", "soul", "funk", "punk", "dance", "house", "disco",
    "edm", "folk", "alternative", "r&b", "trap", "techno", "lo-fi", "dubstep", "k-pop",
    "latin", "acoustic", "instrumental", "chill", "hard rock"
]

genres = st.multiselect("Select Genres (optional):", genre_choices)
date_range = st.text_input("Date Range (e.g., 2000-2025):")
num_songs = st.number_input("Number of Songs:", min_value=1, max_value=100, value=20)
notes = st.text_input("Enter Notes (describe mood or vibe, optional):")

# --- Generate Playlist Button ---
if st.button("Generate Playlist"):
    if not st.session_state.selected_artists and not genres:
        st.error("⚠️ Please select at least one Artist or Genre to generate a playlist!")
    else:
        artist_ids = [st.session_state.artist_id_mapping[artist] for artist in st.session_state.selected_artists]
        artist_names = st.session_state.selected_artists

        candidate_songs = fetch_candidate_songs(sp, artist_ids, artist_names, genres, date_range)
        

        if not candidate_songs:
            st.error("⚠️ No songs found matching your inputs. Try changing artist/genre/date range.")
        else:
            st.success(f"✅ Fetched {len(candidate_songs)} candidate songs from Spotify!")
            

            if len(candidate_songs) < num_songs:
                st.warning(f"⚠️ Only {len(candidate_songs)} songs available, but you requested {num_songs}.")

            selected_songs = generate_playlist_songs(candidate_songs, notes, num_songs, artist_names)
            
            # --- Find Track URIs ---
            track_uris = []
            for song in selected_songs:
                try:
                    clean_song = re.sub(r'^\d+\.\s*', '', song).strip()
                    if "-" in clean_song:
                        title, artist = clean_song.split("-", 1)
                        title = title.strip()
                        artist = artist.strip()
                    else:
                        title = clean_song
                        artist = ""

                    query = f'track:"{title}" artist:"{artist}"' if artist else f'track:"{title}"'
                    result = sp.search(q=query, type='track', limit=1)

                    if not result['tracks']['items']:
                        result = sp.search(q=title, type='track', limit=1)

                    if result['tracks']['items']:
                        track_uris.append(result['tracks']['items'][0]['uri'])
                    else:
                        st.warning(f"⚠️ Could not find: {title} by {artist}")

                except Exception as e:
                    st.error(f"⚠️ Skipping problematic song: {song}")

            # --- Create Playlist ---
            if track_uris:
                playlist_name = generate_playlist_name(artist_names, genres, notes)
                user_id = sp.me()['id']
                playlist = sp.user_playlist_create(user=user_id, name=playlist_name)
                sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)
                st.success(f"🎉 Playlist '{playlist_name}' created successfully!")
                st.markdown(f"[🔗 Open Playlist in Spotify]({playlist['external_urls']['spotify']})")
            else:
                st.error("⚠️ Could not create playlist. No matching songs found.")
