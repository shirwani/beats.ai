import requests
import base64
from utils import *

class Spotify:
    def __init__(self):
        secrets = read_from_json_file("./secrets/secrets.json")
        self.client_id = secrets["spotify"]["client_id"]
        self.client_secret = secrets["spotify"]["client_secret"]
        self.access_token = self.get_access_token()

        cfg = read_from_json_file('config.json')
        self.MAX_TRACKS = cfg['spotify']['max_tracks']
        self.MAX_ALBUMS = cfg['spotify']['max_albums']


    def get_access_token(self):
        """
        Get access token from Spotify
        """
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode('ascii')).decode('ascii')

        # Request token
        url = 'https://accounts.spotify.com/api/token'
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {'grant_type': 'client_credentials'}
        response = requests.post(url, headers=headers, data=data)
        #print(response)
        return response.json()['access_token']

    def search_tracks_by_artist(self, artist_name="Kendrick Lamar"):
        """
        Search Spotify for artist and get a list of song for the artist
        Shove list of songs in the database
        """
        search_url = f'https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1'

        headers = {'Authorization': f'Bearer {self.access_token}'}

        response = requests.get(search_url, headers=headers)
        artist_data = response.json()

        # Get the artist's Spotify ID
        artist_id = artist_data['artists']['items'][0]['id']

        # Get albums for the artist
        albums_url = f'https://api.spotify.com/v1/artists/{artist_id}/albums?limit={self.MAX_ALBUMS}'
        response = requests.get(albums_url, headers=headers)
        albums_data = response.json()

        # Get the track details for each album
        all_tracks = []
        for album in albums_data['items']:
            print(f"Album: {album['name']}")
            album_id = album['id']
            tracks_url = f'https://api.spotify.com/v1/albums/{album_id}/tracks'
            tracks_response = requests.get(tracks_url, headers=headers)
            tracks_data = tracks_response.json()

            for track in tracks_data['items']:
                print(f"    {track['name']}")
                all_tracks.append({
                    'title': track['name'],
                    'artist': artist_name
                    #'id': track['id'],
                    #'popularity': track['popularity'],  # Popularity score (not exact streams, but useful)
                })

        # Sort tracks by popularity
        # all_tracks_sorted = sorted(all_tracks, key=lambda x: x['popularity'], reverse=True)

        return all_tracks[:self.MAX_TRACKS]


if __name__ == '__main__':
    # Search Spotify for tracks by artist
    spotify = Spotify()
    tracks = spotify.search_tracks_by_artist(artist_name="Kendrick Lamar")
    for track in tracks:
        #pass
        print(f"{track['artist']} {track['title']}")
