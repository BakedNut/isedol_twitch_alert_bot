import telegram as tel
import requests
import asyncio
from json import loads

print('ISEDOL CATEGORY ALERT START')

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

bot.sendMessage(chat_id=chat_id, text = "카테고리 알림봇이 (재)시작되었습니다.")

async def isedol_alert(mem_num):
    ment = '{}님의 카테고리가 변경되었습니다'.format(isedol_krname[mem_num])
    check = 0

    # Define pre_category
    while check == 0:
        try:
            headers = {'client-id': twitch_client_id, 'Authorization': authorization}
            response_channel = requests.get('https://api.twitch.tv/helix/channels?broadcaster_id=' + isedol_bc_id[mem_num], headers=headers)
            pre_category = loads(response_channel.text)['data'][0]['game_name']
            print(isedol_krname[mem_num] + ' pre_category define success')
            check = 1
        except:
            print(isedol_krname[mem_num] + ' pre_category define fail... Retry')
            check = 0
        await asyncio.sleep(sleeptime)
    
    print(isedol_krname[mem_num] + " category change alert ready")
    
    # Check Title
    while True:
        headers = {'client-id': twitch_client_id, 'Authorization': authorization}
        response_channel = requests.get('https://api.twitch.tv/helix/channels?broadcaster_id=' + isedol_bc_id[mem_num], headers=headers)
        current_category = loads(response_channel.text)['data'][0]['game_name']
        # print(response_channel.text)
        try:
            if current_category != pre_category:
                bot.sendMessage(chat_id=chat_id, text = ment
                                + '\n이전 카테고리 : ' + pre_category
                                + '\n현재 카테고리 : ' + current_category
                                + '\nhttps://www.twitch.tv/' + isedol_id[mem_num])
                pre_category = current_category
                print(isedol_krname[mem_num] + " Category is changed")
            else:
                print(isedol_krname[mem_num] + " Category is not changed")
        except:
            print(isedol_krname + ' Offline')
            check = 0
            while check == 0:
                try:
                    headers = {'client-id': twitch_client_id, 'Authorization': authorization}
                    response_channel = requests.get('https://api.twitch.tv/helix/streams?user_login=' + isedol_id[mem_num], headers=headers)
                    pre_category = loads(response_channel.text)['data'][0]['game_name']
                    print(isedol_krname[mem_num] + ' pre_category define success')
                    check = 1
                except:
                    print(isedol_krname[mem_num] + ' pre_category define fail... Retry')
                    check = 0
                await asyncio.sleep(sleeptime)
        
        await asyncio.sleep(sleeptime)

async def main():
    try:
        print("Ready on Notification")
        # await asyncio.gather(isedol_alert(1)) # This line is only test
        await asyncio.gather(isedol_alert(0), isedol_alert(1), isedol_alert(2), isedol_alert(3), isedol_alert(4), isedol_alert(5), isedol_alert(6))
    except:
        asyncio.run(main())

asyncio.run(main())