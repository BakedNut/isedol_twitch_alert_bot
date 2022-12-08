import connect
import telegram as tel
import requests
import asyncio
from json import loads

print('ISEDOL ON-OFFLINE ALERT START')

# API Authorization
Auth = connect.twAPIAutho()
Auth.start()

# Connect Telegram
TG = connect.ConnectTG("private") # Input "private" or "public"
bot = TG.bot

# Define ID & nickname
isedol_id = ('vo_ine', 'jingburger', 'lilpaaaaaa', 'cotton__123', 'gosegugosegu', 'viichan6', 'woowakgood')
isedol_bc_id = ('702754423', '237570548', '169700336', '203667951', '707328484', '195641865', '49045679')
isedol_krname = ('아이네', '징버거', '릴파', '주르르', '고세구', '비챤', '우왁굳')

# Define Delay
sleeptime = 5 # 갱신 주기


# Define Category Change Check Function
async def isedol_alert(mem_num):
    ment = '{}님의 카테고리가 변경되었습니다'.format(isedol_krname[mem_num])
    check = 0

    # Define pre_category
    while check == 0:
        try:
            headers = {'client-id': Auth.id, 'Authorization': Auth.authorization}
            response_channel = requests.get('https://api.twitch.tv/helix/channels?broadcaster_id=' + isedol_bc_id[mem_num], headers=headers)
            pre_category = loads(response_channel.text)['data'][0]['game_name']
            print(isedol_krname[mem_num] + ' pre_category define success')
            check = 1
        except:
            print(isedol_krname[mem_num] + ' pre_category define fail... Retry')
            check = 0
        await asyncio.sleep(sleeptime)
    
    print(isedol_krname[mem_num] + " category change alert ready")
    
    # Category change check loop
    while True:
        # Request Channel Data
        try:
            headers = {'client-id': Auth.id, 'Authorization': Auth.authorization}
            response_channel = requests.get('https://api.twitch.tv/helix/channels?broadcaster_id=' + isedol_bc_id[mem_num], headers=headers)
            current_category = loads(response_channel.text)['data'][0]['game_name']
            
            # Category change Check
            if current_category != pre_category:
                # Transmit ment
                bot.sendMessage(chat_id=TG.chat_id, text = ment
                                + '\n현재 카테고리 : ' + current_category
                                + '\n이전 카테고리 : ' + pre_category
                                + '\nhttps://www.twitch.tv/' + isedol_id[mem_num])
                pre_category = current_category
                print(isedol_krname[mem_num] + " Category is changed")
            else:
                print(isedol_krname[mem_num] + " Category is not changed")
        except:
            pass
        
        await asyncio.sleep(sleeptime)

# Define execute function
async def main():
    print("Ready on Notification")
    # await asyncio.gather(isedol_alert(1)) # This line is only test
    await asyncio.gather(isedol_alert(0), isedol_alert(1), isedol_alert(2), isedol_alert(3), isedol_alert(4), isedol_alert(5), isedol_alert(6))

# Start Function
asyncio.run(main())