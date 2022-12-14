import connect
import requests
import asyncio
from json import loads

print('ISEDOL TITLE ALERT START')

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

# Define Title Change Check Function
async def isedol_alert(mem_num):
    # Define Bot Message
    ment = '{}님의 방송 제목이 변경되었습니다'.format(isedol_krname[mem_num])
    
    # Define Title Change check variable
    check = False

    # Define pre_title
    while check == False:
        try:
            headers = {'client-id': Auth.id, 'Authorization': Auth.authorization}
            response_channel = requests.get('https://api.twitch.tv/helix/channels?broadcaster_id=' + isedol_bc_id[mem_num], headers=headers)
            pre_title = loads(response_channel.text)['data'][0]['title']
            print(isedol_krname[mem_num] + ' pre_title define success')
            check = True
        except:
            print(isedol_krname[mem_num] + ' pre_title define fail... Retry')
            check = False
        await asyncio.sleep(sleeptime)
    
    print(isedol_krname[mem_num] + " title change alert ready")

    # Title change check loop
    while True:
        try:
            # Request Channel Data
            headers = {'client-id': Auth.id, 'Authorization': Auth.authorization}
            response_channel = requests.get('https://api.twitch.tv/helix/channels?broadcaster_id=' + isedol_bc_id[mem_num], headers=headers)
            
            # Title change Check
            current_title = loads(response_channel.text)['data'][0]['title']
            if current_title != pre_title:
                bot.sendMessage(chat_id=TG.chat_id, text = ment
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

# Define execute function
async def main():
    print("Ready on Notification")
    await asyncio.gather(isedol_alert(0), isedol_alert(1), isedol_alert(2), isedol_alert(3), isedol_alert(4), isedol_alert(5), isedol_alert(6))

# Start
if __name__ == '__main__':
    asyncio.run(main())
