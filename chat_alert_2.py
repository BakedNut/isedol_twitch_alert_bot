import socket
import telegram as tel
import time
import asyncio

# telegram-bot connect
chat_id = 000000
bot = None #tel.Bot(token="")

# Channels
isedol_id = ("vo_ine", "jingburger", "lilpaaaaaa", "cotton__123", "gosegugosegu", "viichan6", "woowakgood")
isedol_kr = {"vo_ine":"아이네", "jingburger":"징버거", "lilpaaaaaa":"릴파", "cotton__123":"주르르"
             , "gosegugosegu":"고세구", "viichan6":"비챤", "woowakgood":"우왁굳", "chunyangkr":"천양", "111roentgenium":"뢴트게늄"}

async def run(ID):
    SERVER = "irc.twitch.tv"
    PORT = 6667
    PASSWORD = "oauth:xxxxx"  # This needs to be an OAuth token
    USERNAME = ID # Connect This Channel ID
    CHANNEL = USERNAME
    IRC = socket.socket()
    Connecting = True
    IRC.connect((SERVER, PORT))
    IRC.send(
        (
            "PASS " + PASSWORD + "\n" +
            "NICK " + USERNAME + "\n" +
            "JOIN #" + CHANNEL + "\n"
        )
        .encode()
    )
    while Connecting:
        try:
            readbuffer_join = IRC.recv(1024)
            readbuffer_join = readbuffer_join.decode()
            for line in readbuffer_join.split("\n")[0:-1]:
                if ("End of /NAMES list" in line):
                    print("Connected")
                    Connecting = False
        except:
            print("{} Connecting Fail.. Retry".format(ID))
            await asyncio.sleep(5)
            Connecting = True
                
    while True:
        try:
            readbuffer = IRC.recv(1024).decode()
        except:
            readbuffer = ""
        for line in readbuffer.split("\r\n"):
            if "PRIVMSG" in line:
                separate = line.split(":", 2)
                user = separate[1].split("!", 1)[0]
                try:
                    message = line.split(":", 2)[2]
                except:
                    message = ""
                print(f'{ID}/{user}: {message}')
            elif "PING" in line:
                print("Received a PING")
                message = "PONG tmi.twitch.tv\r\n".encode()
                IRC.send(message)
                print("Sent a PONG")
        await asyncio.sleep(0.001)

async def main():
    try:
        print("Ready on Notification")
        # await asyncio.gather(isedol_alert(1)) # This line is only test
        await asyncio.gather(run('zilioner'), run('pjs9073'))
    except:
        asyncio.run(main())

asyncio.run(main())