from googleapiclient.discovery import build
# pip install google-api-python-client
import yt_dlp
from utils import *
import time
from pathlib import Path

class Youtube:
    def __init__(self):
        secrets = read_from_json_file("./secrets/secrets.json")
        self.api_key = secrets["youtube"]["api_key"]
        self.cookiefile = './cookies/youtube_cookies.txt'
        self.download_youtube_cookies()

    def download_youtube_cookies(self):
        """
        Download cookies from Youtube
        """
        delete_file(self.cookiefile)
        ydl_opts = {
            "cookiesfrombrowser": ("chrome",),
            'extract_flat': True,  # We just want to extract cookies, not download the actual video
            'cookiefile': self.cookiefile,  # Save cookies to the specified file
            'quiet': True,  # Silence the output
        }

        # URL of YouTube, you can replace this with any valid YouTube URL
        youtube_url = 'https://www.youtube.com'

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])  # Download cookies for the YouTube URL
            print(f"Cookies saved to {self.cookiefile}")
            time.sleep(5)
        except Exception as e:
            print(f"An error occurred: {e}")

    @fcn_logger
    def search_track(self, artist, title, channel):
        """
        Search track by artist and title
        :return: track info
        """
        query = f"{artist} {title}"

        # Initialize the YouTube API client
        youtube = build("youtube", "v3", developerKey=self.api_key)

        ############################################
        # Step 1: Search for the video by track name
        ############################################
        search_response = youtube.search().list(
            q=query,
            part="id,snippet",
            type="video",
            maxResults=10  # Get the top 10 results for the track
        ).execute()

        ###############################################################
        # Step 2: Get the video ID of the first search result (default)
        # or
        # Pick the best result - based on publisher
        ###############################################################
        video_id = search_response['items'][0]['id']['videoId']

        for item in search_response['items']:
            print(f"item: {item['snippet']['channelTitle']}")
            if item['snippet']['channelTitle'] == channel:
                video_id = item['id']['videoId']
                break

        # Step 3: Get video details using the video ID
        video_response = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=video_id
        ).execute()

        # Extract useful video data
        video_data = video_response['items'][0]
        print(f"Channel Title: {video_data['snippet']['channelTitle']}")

        track = dict()
        track['artist'] = artist
        track['title'] = title
        track['url'] = f"https://www.youtube.com/watch?v={video_id}"
        track['published_at'] = video_data['snippet']['publishedAt']
        track['publisher'] = video_data['snippet']['channelTitle']
        track['views'] = video_data['statistics'].get('viewCount', 0)
        track['likes'] = video_data['statistics'].get('likeCount', 0)
        track['comments'] = video_data['statistics'].get('commentCount', 0)

        return track

    @fcn_logger
    def download_single_track(self, artist, title, channel):
        """
        Search track by artist name and title, then download it
        """

        track = self.search_track(artist, title, channel)


        # Set the options for yt-dlp
        ydl_opts = {
            #"cookiesfrombrowser": ("chrome",),
            'cookiefile': self.cookiefile,
            'format': 'bestaudio/best',  # Best quality audio
            'outtmpl': f"dataset/downloads/{artist} - {title}.%(ext)s",  # Set output filename format
            'quiet': False,  # Show download progress
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([track['url']])
                print(f"Download complete: {track['url']}")
                file = f"dataset/downloads/{artist} - {title}.mp3"
                if Path(file).exists():
                    track['filename'] = f"{artist} - {title}.mp3"
        except Exception as e:
            print(f"An error occurred: {e}")

        return track

if __name__ == '__main__':
    youtube = Youtube()
    track = youtube.download_single_track(artist="HackaZ Beats", title="Divine Drip", channel="")
    print(track)
