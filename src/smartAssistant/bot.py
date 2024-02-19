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
        elif 'weather' in user_input:
            # Ensure you implement or remove the get_weather method if it's not used
            await turn_context.send_activity("Weather functionality not implemented.")
        else:
            await turn_context.send_activity(f"You said '{turn_context.activity.text}'")

    async def play_song(self, turn_context: TurnContext, song_name: str):
        # This method should handle the logic for playing a song using Spotify's API
        access_token = self.get_spotify_access_token()
        if access_token:
            song_uri = self.search_song(song_name, access_token)
            if song_uri:
                success = self.start_playback(song_uri, access_token)
                if success:
                    await turn_context.send_activity(f"Playing song: {song_name}")
                else:
                    await turn_context.send_activity("Failed to start playback.")
            else:
                await turn_context.send_activity("Song not found.")
        else:
            await turn_context.send_activity("Failed to get Spotify access token.")
        
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
        query = f"{song_name} artist:Justin Bieber".replace(" ", "%20")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"https://api.spotify.com/v1/search?q={song_name}&type=track", headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to search song: {response.json()}")
            return None

        search_results = response.json()
        if 'tracks' in search_results and search_results['tracks']['items']:
            return search_results['tracks']['items'][0]['uri']  # Get the first song's URI
        else:
            print("No tracks found for the given search term.")
            return None

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

    


