import spotipy
import re
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
from flask import Flask, render_template, request
import os
from pytube import YouTube

app = Flask(__name__)

# Replace YOUR_CLIENT_ID and YOUR_CLIENT_SECRET with your actual credentials
client_id = "2b4f7f19e9c549c287f35e11889e3ca6"
client_secret = "b7f69416ddf741f5960ebca06a4f6d36"
youtube_api_key = "AIzaSyBuqP-l-GWFdxmgtKym9TRaQFqVtqqfWfE"

# Create the client credentials manager for Spotify
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Create the YouTube client object
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

# Function to search for YouTube videos based on track title and artist name
def search_youtube_videos(track_title, artist_name):
    # Construct the search query by combining track title and artist name
    search_query = f"{track_title} - {artist_name}"

    request = youtube.search().list(
        q=search_query,
        part='id',
        maxResults=1,
        type='video'
    )
    response = request.execute()
    if 'items' in response:
        video_id = response['items'][0]['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        return video_url
    return None

# Function to download audio from YouTube video and save it as an MP3 file
def download_youtube_audio(youtube_url, output_folder, output_file):
    try:
        # Create a YouTube object
        yt = YouTube(youtube_url)
        
        # Select the first audio stream with the highest quality (for MP3 conversion)
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        
        # Download the audio stream and save it as an MP3 file within the output folder
        mp3_filename = os.path.join(output_folder, f"{output_file}.mp3")  # Add the .mp3 extension to the filename
        audio_stream.download(output_path=output_folder, filename=f"{output_file}.mp3")
        
        print(f"Successfully downloaded and converted {youtube_url} to {mp3_filename}")
    except Exception as e:
        print(f"Error: {e}")
        print(f"Failed to download {youtube_url}")

# Function to retrieve song titles and artist names from the Spotify playlist
def get_song_info(playlist_link):
    playlist_id_pattern = r'^https://open\.spotify\.com/playlist/([a-zA-Z0-9]+)'
    match = re.match(playlist_id_pattern, playlist_link)

    if match:
        playlist_id = match.group(1)
        playlist = sp.playlist(playlist_id)
        playlist_name = playlist['name']
        songs_info = [(track['track']['name'], track['track']['artists'][0]['name']) for track in playlist['tracks']['items']]
        return playlist_name, songs_info
    return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        playlist_link = request.form['playlist_link']
        playlist_name, songs_info = get_song_info(playlist_link)

        if playlist_name and songs_info:
            # Process the songs_info list to find YouTube links and download audio (using your previous code)
            for song_title, artist_name in songs_info:
                youtube_link = search_youtube_videos(song_title, artist_name)
                if youtube_link:
                    print(f"{song_title} - {artist_name} - YouTube Link: {youtube_link}")
                    download_youtube_audio(youtube_link, playlist_name, f"{song_title} - {artist_name}")
                else:
                    print(f"{song_title} - {artist_name} - No YouTube video found for this track.")
            return "Success"
        else:
            error_message = "Invalid playlist link. Please enter a valid Spotify playlist link or ID."
            return error_message

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
