import telegram as tel
import requests
import asyncio
from json import loads

print('ISEDOL ON-OFFLINE ALERT START')

twitch_client_id = '' # 본인 twitch API ID 입력
twitch_client_secret = '' # 본인 twitch API secret key 입력

oauth_key = requests.post("https://id.twitch.tv/oauth2/token?client_id=" + twitch_client_id + "&client_secret=" + twitch_client_secret + "&grant_type=client_credentials")
access_token = loads(oauth_key.text)["access_token"]
token_type = 'Bearer '
authorization = token_type + access_token
print(authorization)

chat_id = 000000
#본인 텔레그램 서버 or 채팅창 id 입력
#채팅창, 서버마다 다르므로 참고할 것 / https://api.telegram.org/bot[token입력]/getUpdates 여기서 확인

bot = tel.Bot(token="") # "" 안에 본인 텔레그램 봇 토큰 입력

isedol_id = ('vo_ine', 'jingburger', 'lilpaaaaaa', 'cotton__123', 
             'gosegugosegu', 'viichan6', 'woowakgood')

isedol_krname = ('아이네', '징버거', '릴파', '주르르', '고세구', '비챤', '우왁굳')

sleeptime = 5 # 갱신 주기

bot.sendMessage(chat_id=chat_id, text = "온-오프 알림봇이 (재)시작되었습니다")

async def isedol_alert(mem_num):
    ment = '{}님이 방송을 시작하셨습니다!'.format(isedol_krname[mem_num])
    offment = '{}님이 방송을 종료하셨습니다'.format(isedol_krname[mem_num])
    
    print(isedol_krname[mem_num] + " alert ready")

    check = False
    
    while True:
        headers = {'client-id': twitch_client_id, 'Authorization': authorization}
        response_channel = requests.get('https://api.twitch.tv/helix/streams?user_login=' + isedol_id[mem_num], headers=headers)
        # print(response_channel.text) 터미널 창 더러워져서 주석처리함
        try:
            if loads(response_channel.text)['data'][0]['type'] == 'live' and check == False:
                bot.sendMessage(chat_id=chat_id, text = ment
                                + '\n방송제목 : ' + loads(response_channel.text)['data'][0]['title']
                                + '\n카테고리 : ' + loads(response_channel.text)['data'][0]['game_name']
                                + '\nhttps://www.twitch.tv/' + isedol_id[mem_num])
                print(isedol_krname[mem_num] + " Online")
                check = True
        except:
            if check == True:
                bot.sendMessage(chat_id=chat_id, text = offment)
            print(isedol_krname[mem_num] + " Offline")
            check = False
        
        await asyncio.sleep(sleeptime)

async def main():
    print("Ready on Notification")
    await asyncio.gather(isedol_alert(0), isedol_alert(1), isedol_alert(2), isedol_alert(3), isedol_alert(4), isedol_alert(5), isedol_alert(6))

asyncio.run(main())