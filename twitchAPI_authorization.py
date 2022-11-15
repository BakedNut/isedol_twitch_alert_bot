# twitch API 인증 스크립트

import requests
from json import loads

twitch_client_id = '' # 본인 twitch API ID 입력
twitch_client_secret = '' # 본인 twitch API secret key 입력

oauth_key = requests.post("https://id.twitch.tv/oauth2/token?client_id=" + twitch_client_id + "&client_secret=" + twitch_client_secret + "&grant_type=client_credentials")
access_token = loads(oauth_key.text)["access_token"]
token_type = 'Bearer '
authorization = token_type + access_token
print(authorization)