import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Generate Playlist Name ---
def generate_playlist_name(artists, genres, mood=""):
    input_text = f"""
Create a creative, engaging playlist name for a Spotify playlist.
Details:
- Featuring artists: {', '.join(artists) if artists else 'various artists'}
- Genres: {', '.join(genres) if genres else 'mixed genres'}
- Mood: {mood if mood else 'general vibe'}

Rules:
- Keep it short and catchy (3 to 8 words maximum).
- Do not mention the word 'playlist'.
- Focus on the vibe or feeling of the music.

Just return the playlist name.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": input_text}]
    )
    return response.choices[0].message.content.strip()


# --- Generate Playlist Songs ---
def generate_playlist_songs(candidate_songs, notes, num_songs, artist_names):
    input_prompt = f"""
You are given a list of real Spotify songs below.

TASK:
- Pick exactly {num_songs} songs that match the mood: "{notes}".
- Distribute songs fairly: Pick roughly eaqual number of songs for each artist in {artist_names}.
- ONLY select songs from the given list. DO NOT invent any new songs or artists.
- Make sure to fit the vibe/mood described.
- Include at least 2 songs from each artist in {artist_names}if possible.
- DO NOT add numbers or bullet points before the songs.
- Do not select the same song more than once.
- Do not include any extra text or explanations in the response.
- Each line must follow this format exactly: Song Title - Artist Name

Songs List:
{chr(10).join(candidate_songs)}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": input_prompt}]
    )

    playlist_text = response.choices[0].message.content.strip()
    songs = [line.strip() for line in playlist_text.split("\n") if line.strip()]
    return songs
