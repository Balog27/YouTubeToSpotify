import requests
import urllib.parse

class SpotifyClient(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def search_song(self, artist, track):
        query = f"artist:{urllib.parse.quote(artist)} track:{urllib.parse.quote(track)}"
        url = f"https://api.spotify.com/v1/search?q={query}&type=track"
        response = requests.get(url, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        })
        response_json = response.json()
        if 'tracks' in response_json:
            results = response_json['tracks']['items']
            if results:
                return results[0]['id']
        raise Exception(f"No song found for {artist} - {track}")

    def add_song_to_spotify(self, song_id):
        url = "https://api.spotify.com/v1/me/tracks"
        response = requests.put(url, json={
            "ids": [song_id]
        }, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        })
        return response.ok