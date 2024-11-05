import os
from youtubeClient import YouTubeClient
from spotifyClient import SpotifyClient

def run():
    # Get a list of our playlists from YouTube
    youtube_client = YouTubeClient(r'C:\Users\Balog David\Personal work\SpotifyYt\creds\client_secret.json')
    spotify_client = SpotifyClient(os.getenv('SPOTIFY_AUTH_TOKEN'))
    playlists = youtube_client.get_playlists()

    # Ask which playlist we want to get the music video from
    for index, pl in enumerate(playlists):
        print(f"{index}: {pl.title}")

    choice = int(input("Enter your choice: "))
    chosen_playlist = playlists[choice]
    print(f"You selected: {chosen_playlist.title}")

    # For each video in the playlist, get the song information from YouTube
    songs = youtube_client.get_playlist_videos(chosen_playlist.id)
    print(f"Attempting to add {len(songs)} songs")

    # Search for songs on Spotify
    for song in songs:
        print(f"Searching for {song.artist} - {song.song} on Spotify")
        try:
            spotify_song_id = spotify_client.search_song(song.artist, song.song)
            if spotify_song_id:
                added = spotify_client.add_song_to_spotify(spotify_song_id)
                if added:
                    print(f"Added {song.artist} - {song.song} to Spotify")
                else:
                    print(f"Failed to add {song.artist} - {song.song} to Spotify")
            else:
                print(f"No Spotify ID found for {song.artist} - {song.song}")
        except Exception as e:
            print(f"Error searching for {song.artist} - {song.song}: {e}")

if __name__ == '__main__':
    run()