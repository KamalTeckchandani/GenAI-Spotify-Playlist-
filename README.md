🎵 GenAI Custom Playlist Creator
An AI-powered Spotify playlist creator where users can:

Search and select multiple verified artists from Spotify,

Define vibes/moods (like "chill", "workout", "party"),

Automatically generate a playlist with songs matching the mood,

Create and save the playlist directly into their Spotify account.

Built with Python, Streamlit, OpenAI GPT, and Spotify Web API.

📸 Demo

🚀 Features
Live Spotify Artist Search
Search any artist by name, select multiple verified artists directly from Spotify results.

Mood-based AI Song Selection
Using OpenAI GPT to smartly select songs from the searched artists that best match your described mood.

Flexible Options
Customize:

Genres (optional),

Date ranges (e.g., 2000–2025),

Number of songs (1–100).

One-click Spotify Playlist Creation
Automatically saves the curated playlist to your personal Spotify account.

🛠️ Tech Stack
Frontend	Backend	AI Engine	APIs
Streamlit	Python	OpenAI GPT-3.5 Turbo	Spotify Web API

📦 Installation
Clone the repository


git clone https://github.com/your-username/genai-playlist-creator.git
cd genai-playlist-creator
Create a virtual environment (optional but recommended)


python -m venv env
source env/bin/activate    # On Windows: env\Scripts\activate
Install dependencies


pip install -r requirements.txt
Set up your environment variables

Create a .env file with the following contents:

dotenv
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8501/callback
OPENAI_API_KEY=your_openai_api_key
Run the application


streamlit run app.py
🧩 Folder Structure
bash
Copy
Edit
├── app.py                  # Main Streamlit application
├── spotify_utils.py         # Spotify client and data fetching functions
├── genai_utils.py           # GPT-based song selection logic
├── .env                     # Environment variables (local use only)
├── requirements.txt         # Required Python packages
└── README.md                # Project documentation
📝 Requirements
Python 3.9+

Spotify Developer Account

OpenAI API Key

Internet Connection

⚡ How it Works
Search your favorite artist(s) using the search bar.

Pick from live Spotify results (verified, correct artists).

Define the mood (e.g., "chill vibes", "party mood", "energetic workout").

AI selects the best-fit songs.

Create and save the playlist directly to your Spotify account!

🙌 Acknowledgements
Streamlit

Spotify Web API

OpenAI

Special thanks to everyone who contributed to this ecosystem!

📜 License
This project is licensed under the MIT License.
Feel free to fork, use, and improve it!

✨ Future Enhancements
Playlist cover image generation using AI

Mood prediction based on audio analysis

Smart shuffle options (slow start → energetic end, etc.)

Save past playlists and recommend new ones

📬 Contact
If you like the project or want to collaborate, feel free to connect:

GitHub: (https://github.com/KamalTeckchandani)

LinkedIn: https://www.linkedin.com/in/kamal-teckchandani/

🔥 Let's make music
