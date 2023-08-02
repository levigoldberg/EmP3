import spotify_playlist_parser
from googleapiclient.discovery import build

# Replace YOUR_YOUTUBE_API_KEY with your actual YouTube API key
youtube_api_key = "AIzaSyBuqP-l-GWFdxmgtKym9TRaQFqVtqqfWfE"

# Function to search for YouTube videos based on track title
def search_youtube_videos(track_title):
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    request = youtube.search().list(
        q=track_title,
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

# Example usage:
if __name__ == "__main__":
    # Replace 'YOUR_SPOTIFY_PLAYLIST_LINK_OR_ID' with the actual Spotify playlist link or ID
    playlist_link = "YOUR_SPOTIFY_PLAYLIST_LINK_OR_ID"

    # Extract song titles from the playlist using the function from spotify_playlist_parser.py
    song_titles = spotify_playlist_parser.get_song_titles(playlist_link)

    print("Songs in the playlist:")
    for title in song_titles:
        youtube_link = search_youtube_videos(title)
        if youtube_link:
            print(f"{title} - YouTube Link: {youtube_link}")
        else:
            print(f"{title} - No YouTube video found for this track title.")
