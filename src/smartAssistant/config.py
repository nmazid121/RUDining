#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

    SPOTIFY_CLIENT_ID = "e48aa139cf814a1c8f53a991f60b5fe8"
    SPOTIFY_CLIENT_SECRET = "1c23ef206ef74c94a4f423e639845be7"
    SPOTIFY_REDIRECT_URI = "http://localhost:3978/callback"