# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
import traceback
from datetime import datetime

from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity, ActivityTypes

from bot import MyBot
from config import DefaultConfig
from requests_oauthlib import OAuth2Session

CONFIG = DefaultConfig()

# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)


# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity(
        "To continue to run this bot, please fix the bot source code."
    )
    # Send a trace activity if we're talking to the Bot Framework Emulator
    if context.activity.channel_id == "emulator":
        # Create a trace activity that contains the error object
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.now(timezone.utc),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        # Send a trace activity, which will be displayed in Bot Framework Emulator
        await context.send_activity(trace_activity)


ADAPTER.on_turn_error = on_error

# Create the Bot
BOT = MyBot()


# Listen for incoming requests on /api/messages
async def messages(req: Request) -> Response:
    # Main bot message handler.
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=201)


# Define your Spotify scopes and client secret (ensure these are securely stored)
SPOTIFY_SCOPES = ["user-read-playback-state", "user-modify-playback-state", "playlist-read-private"]
SPOTIFY_CLIENT_SECRET = "1c23ef206ef74c94a4f423e639845be7"  # Your client secret from your Spotify app settings

# Spotify callback route
async def spotify_callback(req: Request) -> Response:
    code = req.query.get('code')
    spotify = OAuth2Session(CONFIG.SPOTIFY_CLIENT_ID, redirect_uri=CONFIG.SPOTIFY_REDIRECT_URI)
    try:
        # Fetch the access token using the authorization code
        token = spotify.fetch_token(
            'https://accounts.spotify.com/api/token',
            client_secret=CONFIG.SPOTIFY_CLIENT_SECRET,
            code=code
        )
        
        # Write the access token to a file
        with open("spotify_access_token.txt", "w") as file:
            file.write(token['access_token'])
        
        # Respond to the request indicating successful authentication
        return json_response({"message": "Authentication successful"})
    except Exception as e:
        # Handle errors (e.g., invalid code) and respond accordingly
        return json_response({"error": "Authentication failed", "details": str(e)}, status=400)



# Spotify login route
async def spotify_login(req: Request) -> Response:
    spotify = OAuth2Session(CONFIG.SPOTIFY_CLIENT_ID, scope=SPOTIFY_SCOPES, redirect_uri="http://localhost:3978/callback")
    authorization_url, state = spotify.authorization_url('https://accounts.spotify.com/authorize')
    # Redirect the user to Spotify's authorization page
    return web.HTTPFound(location=authorization_url)

APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)
APP.router.add_get("/spotify-login", spotify_login)
APP.router.add_get("/callback", spotify_callback)

if __name__ == "__main__":
    try:
        web.run_app(APP, host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error
