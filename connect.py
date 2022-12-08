# twitch API 인증, telegram 연결 Class

import requests
from json import loads
import telegram as tel

class twAPIAutho():
    id = '' # twitch_client_id 입력
    secret = '' # twitch_client_secret 입력
    def start(self):
        self.oauth_key = requests.post("https://id.twitch.tv/oauth2/token?client_id=" + twAPIAutho.id + "&client_secret=" + twAPIAutho.secret + "&grant_type=client_credentials")
        self.access_token = loads(self.oauth_key.text)["access_token"]
        self.token_type = 'Bearer '
        self.authorization = self.token_type + self.access_token
        print(self.authorization)
        
class ConnectTG():
    bot = tel.Bot(token="") # "" 안에 본인 텔레그램 봇 토큰 입력
    def __init__(self, purpose):
        self.purpose = purpose
        if self.purpose == "private":
            self.chat_id = 00000000 # 개인 봇 채팅방 ID 입력
        elif self.purpose == "public":
            self.chat_id = 00000000 # 봇 공지방 ID 입력
        else:
            raise KeyError()
