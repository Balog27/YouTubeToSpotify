import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import yt_dlp as youtube_dl

class Playlist:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def __str__(self):
        return f"{self.title}"

class Song:
    def __init__(self, artist, song):
        self.artist = artist
        self.song = song

    def __str__(self):
        return f"{self.artist} : {self.song}"

class YouTubeClient(object):
    def __init__(self, credentials_location):
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            credentials_location, scopes)
        credentials = flow.run_console()
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        self.youtube_client = youtube_client

    def get_playlists(self):
        request = self.youtube_client.playlists().list(
            part="id,snippet",
            maxResults=50,
            mine=True
        )
        response = request.execute()

        playlists = [Playlist(item['id'], item['snippet']['title']) for item in response['items']]
        return playlists

    def get_playlist_videos(self, playlist_id):
        songs = []
        request = self.youtube_client.playlistItems().list(
            playlistId=playlist_id,
            part="id,snippet",
            maxResults=50
        )
        response = request.execute()

        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            print(f"Processing video ID: {video_id}")
            artist, song = self.get_artist_and_songs_from_video(video_id)
            if artist and song:
                print(f"Found song: {artist} - {song}")
                songs.append(Song(artist, song))
            else:
                print(f"No song information found for video ID: {video_id}")

        return songs

    def get_artist_and_songs_from_video(self, video_id):
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        ydl_opts = {
            'quiet': True,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegMetadata',
            }]
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                video = ydl.extract_info(youtube_url, download=False)
                title = video.get('title')
                artist = video.get('artist')
                print(f"Extracted title for video ID {video_id}: title={title}, artist={artist}")

                if not artist or not title:
                    # Fallback to parsing the title if metadata is not available
                    title = title or ""
                    title = title.replace("(Official Music Video)", "").strip()
                    parts = title.split('-')
                    if len(parts) >= 2:
                        artist = parts[0].strip()
                        song = parts[1].strip()
                    else:
                        artist, song = None, None
                else:
                    song = title
            except Exception as e:
                print(f"Error extracting info for video ID {video_id}: {e}")
                artist, song = None, None
        return artist, song


