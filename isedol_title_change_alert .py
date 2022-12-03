import telegram as tel
import requests
import asyncio
from json import loads

print('ISEDOL TITLE ALERT START')

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

isedol_bc_id = ('702754423', '237570548', '169700336', '203667951', '707328484', '195641865', '49045679')

isedol_krname = ('아이네', '징버거', '릴파', '주르르', '고세구', '비챤', '우왁굳')

sleeptime = 5 # 갱신 주기

async def isedol_alert(mem_num):
    ment = '{}님의 방송 제목이 변경되었습니다'.format(isedol_krname[mem_num])
    check = 0

    # Define pre_title
    while check == 0:
        try:
            headers = {'client-id': twitch_client_id, 'Authorization': authorization}
            response_channel = requests.get('https://api.twitch.tv/helix/channels?broadcaster_id=' + isedol_bc_id[mem_num], headers=headers)
            pre_title = loads(response_channel.text)['data'][0]['title']
            print(isedol_krname[mem_num] + ' pre_title define success')
            check = 1
        except:
            print(isedol_krname[mem_num] + ' pre_title define fail... Retry')
            check = 0
        await asyncio.sleep(sleeptime)
    
    print(isedol_krname[mem_num] + " title change alert ready")

    # Check Title
    while True:
        try:
            headers = {'client-id': twitch_client_id, 'Authorization': authorization}
            response_channel = requests.get('https://api.twitch.tv/helix/channels?broadcaster_id=' + isedol_bc_id[mem_num], headers=headers)
            current_title = loads(response_channel.text)['data'][0]['title']
            if current_title != pre_title:
                bot.sendMessage(chat_id=chat_id, text = ment
                                + '\n현재 방송 제목 : ' + current_title
                                + '\n이전 방송 제목 : ' + pre_title
                                + '\nhttps://www.twitch.tv/' + isedol_id[mem_num])
                pre_title = current_title
                print(isedol_krname[mem_num] + " Title is changed")
            else:
                print(isedol_krname[mem_num] + " Title is not changed")
        except:
            pass
        
        await asyncio.sleep(sleeptime)

async def main():
    print("Ready on Notification")
    # await asyncio.gather(isedol_alert(1)) # This line is only test
    await asyncio.gather(isedol_alert(0), isedol_alert(1), isedol_alert(2), isedol_alert(3), isedol_alert(4), isedol_alert(5), isedol_alert(6))

asyncio.run(main())