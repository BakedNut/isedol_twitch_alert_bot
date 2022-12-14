import connect
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
isedol_krname = ('아이네', '징버거', '릴파', '주르르', '고세구', '비챤', '우왁굳')

# Define Delay
sleeptime = 5 # 갱신 주기

# Define On-Offline Check Function
async def isedol_alert(mem_num):
    # Define Bot Message
    ment = '{}님이 방송을 시작하셨습니다!'.format(isedol_krname[mem_num])
    offment = '{}님이 방송을 종료하셨습니다'.format(isedol_krname[mem_num])
    
    # Output alert ready message
    print(isedol_krname[mem_num] + " alert ready")

    # Define On-Offline check variable
    check = False
    
    # On-Offline check loop
    while True:
        try:
            # Request Channel Data
            headers = {'client-id': Auth.id, 'Authorization': Auth.authorization}
            response_channel = requests.get('https://api.twitch.tv/helix/streams?user_login=' + isedol_id[mem_num], headers=headers)
            
            # On-Offline Check
            if loads(response_channel.text)['data'][0]['type'] == 'live' and check == False:
                # Transmit ment
                bot.sendMessage(chat_id=TG.chat_id, text = ment
                                + '\n방송제목 : ' + loads(response_channel.text)['data'][0]['title']
                                + '\n카테고리 : ' + loads(response_channel.text)['data'][0]['game_name']
                                + '\nhttps://www.twitch.tv/' + isedol_id[mem_num])
                print(isedol_krname[mem_num] + " Online")
                check = True
        # If Channel is Offline, error occurred
        except:
            # If On-Offline check is True, Transmit offment
            if check == True:
                bot.sendMessage(chat_id=TG.chat_id, text = offment)
            print(isedol_krname[mem_num] + " Offline")
            check = False
        
        # Delay
        await asyncio.sleep(sleeptime)

# Define execute function
async def main():
    print("Ready on Notification")
    await asyncio.gather(isedol_alert(0), isedol_alert(1), isedol_alert(2), isedol_alert(3), isedol_alert(4), isedol_alert(5), isedol_alert(6))

# Start
if __name__ == '__main__':
    asyncio.run(main())
