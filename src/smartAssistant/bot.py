from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
import requests

class MyBot(ActivityHandler):
    # Retained the initial greeting for new members
    async def on_members_added_activity(self, members_added: ChannelAccount, turn_context: TurnContext):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome! Use this link to link your spotify account: http://localhost:3978/spotify-login")

    # Updated on_message_activity function
    async def on_message_activity(self, turn_context: TurnContext):
        user_input = turn_context.activity.text.lower()
        
        if 'play' in user_input:
            song_name = user_input.replace('play', '').strip()
            await self.play_song(turn_context, song_name)
        elif 'pause' in user_input:
            await self.pause_song(turn_context)
        elif 'resume' in user_input:
            await self.resume_song(turn_context)
        elif 'queue' in user_input:
            song_name = user_input.replace('queue', '').strip()
            await self.queue_song(turn_context, song_name) 
        elif 'skip' in user_input:
            await self.skip_song(turn_context)
        elif 'previous' or 'go back' in user_input:
            await self.previous_song(turn_context)
        elif 'weather' in user_input:
            # Ensure you implement or remove the get_weather method if it's not used
            await turn_context.send_activity("Weather functionality not implemented.")
        else:
            await turn_context.send_activity(f"You said '{turn_context.activity.text}'")

    async def play_song(self, turn_context: TurnContext, song_name: str):
        access_token = self.get_spotify_access_token()
        if not access_token:
            await turn_context.send_activity("Failed to get Spotify access token.")
            return

        song_uri, track_name, artist_name = self.search_song(song_name, access_token)  # Updated to fetch track and artist names
        if song_uri:
            success = self.start_playback(song_uri, access_token)
            if success:
                # Updated to use the fetched track name and artist name
                await turn_context.send_activity(f"Playing song: {track_name} by {artist_name}")
            else:
                await turn_context.send_activity("Failed to start playback.")
        else:
            await turn_context.send_activity("Song not found.")
        
    async def pause_song(self, turn_context: TurnContext):
        await turn_context.send_activity("Music paused.")

    def get_spotify_access_token(self):
        # Implement OAuth flow to get an access token from Spotify
        # This should return a valid access token or None if the process fails
        try:
            with open("spotify_access_token.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            print("Access token file not found.")
            return None

    def search_song(self, song_name, access_token):
        query = f"{song_name}".replace(" ", "%20")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"https://api.spotify.com/v1/search?q={query}&type=track", headers=headers)
    
        if response.status_code == 200:
            search_results = response.json()
            items = search_results['tracks']['items']
            if items:
                # Assuming you want the first search result
                first_item = items[0]
                track_uri = first_item['uri']
                track_name = first_item['name']
                artist_name = first_item['artists'][0]['name']  # Assuming the first artist is the primary one
                return track_uri, track_name, artist_name
        return None, None, None

    def start_playback(self, song_uri, access_token):
        headers = {"Authorization": f"Bearer {access_token}"}
        data = {"uris": [song_uri]}
        response = requests.put("https://api.spotify.com/v1/me/player/play", headers=headers, json=data)
        return response.ok
    
    async def pause_song(self, turn_context: TurnContext):
        access_token = self.get_spotify_access_token()
        if access_token:
            headers = {"Authorization": f"Bearer {access_token}"}
            pause_endpoint = "https://api.spotify.com/v1/me/player/pause"
            response = requests.put(pause_endpoint, headers=headers)
            if response.status_code in [200, 204]:
                await turn_context.send_activity("Music paused.")
            else:
                await turn_context.send_activity(f"Failed to pause music: {response.json()}")
        else:
            await turn_context.send_activity("Failed to get Spotify access token.")

    async def resume_song(self, turn_context: TurnContext):
        access_token = self.get_spotify_access_token()
        if access_token:
            headers = {"Authorization": f"Bearer {access_token}"}
            resume_endpoint = "https://api.spotify.com/v1/me/player/play"
            response = requests.put(resume_endpoint, headers=headers)
            if response.status_code in [200, 204]:
                await turn_context.send_activity("Music resumed.")
            else:
                await turn_context.send_activity(f"Failed to resume music: {response.json()}")
        else:
            await turn_context.send_activity("Failed to get Spotify access token.")

    async def skip_song(self, turn_context: TurnContext):
        access_token = self.get_spotify_access_token()
        if access_token:
            headers = {"Authorization": f"Bearer {access_token}"}
            skip_endpoint = "https://api.spotify.com/v1/me/player/next"
            response = requests.post(skip_endpoint, headers=headers)
            if response.status_code in [200, 204]:
                await turn_context.send_activity("Music skipped.")
            else:
                await turn_context.send_activity(f"Failed to skip music: {response.json()}")
        else:
            await turn_context.send_activity("Failed to get Spotify access token.")

    async def previous_song(self, turn_context: TurnContext):
        access_token = self.get_spotify_access_token()
        if access_token:
            headers = {"Authorization": f"Bearer {access_token}"}
            previous_endpoint = "https://api.spotify.com/v1/me/player/previous"
            response = requests.post(previous_endpoint, headers=headers)
            if response.status_code in [200, 204]:
                await turn_context.send_activity("Music skipped to previous.")
            else:
                await turn_context.send_activity(f"Failed to skip music: {response.json()}")
        else:
            await turn_context.send_activity("Failed to get Spotify access token.")

    async def queue_song(self, turn_context: TurnContext, song_name: str):
        access_token = self.get_spotify_access_token()
        if not access_token:
            await turn_context.send_activity("Failed to get Spotify access token.")
            return

        song_uri, track_name, artist_name = self.search_song(song_name, access_token)  # Unpack all returned values
        if song_uri:  # Check if a song URI was successfully retrieved
            headers = {"Authorization": f"Bearer {access_token}"}
            queue_endpoint = f"https://api.spotify.com/v1/me/player/queue?uri={song_uri}"
            response = requests.post(queue_endpoint, headers=headers)

            if response.status_code in [200, 204]:
                await turn_context.send_activity(f"Added '{track_name} by {artist_name}' to the queue.")  # Use track name and artist name in the response
            else:
                error_message = "Failed to queue the song."
                try:
                    # Attempt to parse error message if available
                    error_data = response.json()
                    if error_data.get("error"):
                        error_message += f" Error: {error_data['error'].get('message')}"
                except ValueError:  # Includes json.JSONDecodeError
                    # No additional error info available
                    pass
                await turn_context.send_activity(error_message)
        else:
            await turn_context.send_activity("Song not found.")



    


