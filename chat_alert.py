import connect
import asyncio
from json import loads

print('ISEDOL CHAT ALERT START')

# Connect Telegram
TG = connect.ConnectTG("private") # Input "private" or "public"
bot = TG.bot

# Channels
track = ("vo_ine", "jingburger", "lilpaaaaaa", "cotton__123", "gosegugosegu", "viichan6", "woowakgood", "chunyangkr", "111roentgenium")
isedol_id = ("vo_ine", "jingburger", "lilpaaaaaa", "cotton__123", "gosegugosegu", "viichan6", "woowakgood")
isedol_kr = {"vo_ine":"아이네 ⚪️", "jingburger":"징버거 🟡", "lilpaaaaaa":"릴파 🔵", "cotton__123":"주르르 🟣"
             , "gosegugosegu":"고세구 🦠", "viichan6":"비챤 🟢", "woowakgood":"우왁굳 🐵", "chunyangkr":"천양 🐡", "111roentgenium":"뢴트게늄 ☢"}

async def run(ID):
    SERVER = "irc.twitch.tv"
    PORT = 6667
    IRCread: asyncio.StreamReader
    IRCwrite: asyncio.StreamWriter
    PASSWORD = connect.twAPIAutho.OAuth  # This needs to be an OAuth token
    USERNAME = ID # Connect This Channel ID
    CHANNEL = USERNAME
    Connecting = True
    IRCread, IRCwrite = await asyncio.open_connection(SERVER, PORT)
    IRCwrite.write(
        (
            "PASS " + PASSWORD + "\n" +
            "NICK " + USERNAME + "\n" +
            "JOIN #" + CHANNEL + "\n"
        )
        .encode()
    )
    await IRCwrite.drain()
    
    while Connecting:
        try:
            readbuffer_join = await IRCread.read(1024)
            readbuffer_join = readbuffer_join.decode()
            for line in readbuffer_join.split("\n")[0:-1]:
                if ("End of /NAMES list" in line):
                    print(f"{ID} Connected")
                    Connecting = False
        except:
            print(f'{ID} Connect Fail.. Retry')
            IRCread, IRCwrite = await asyncio.open_connection(SERVER, PORT)
            IRCwrite.write(
                (
                    "PASS " + PASSWORD + "\n" +
                    "NICK " + USERNAME + "\n" +
                    "JOIN #" + CHANNEL + "\n"
                )
                .encode()
            )
            await IRCwrite.drain()
                
    while True:
        readbuffer = await IRCread.read(1024)
        readbuffer = readbuffer.decode()
        for line in readbuffer.split("\r\n"):
            if "PRIVMSG" in line:
                separate = line.split(":", 2)
                user = separate[1].split("!", 1)[0]
                try:
                    message = line.split(":", 2)[2]
                except:
                    message = ""
                if user in isedol_id:
                    if user == USERNAME:
                        bot.sendMessage(chat_id=TG.chat_id, text= isedol_kr[user] + ":\n" + message)
                    else:
                        bot.sendMessage(chat_id=TG.chat_id, text= isedol_kr[user] + " → " + isedol_kr[USERNAME] + ":\n" + message)
            elif "PING" in line:
                print(f"Received a PING : {ID}")
                message = "PONG tmi.twitch.tv\r\n".encode()
                IRCwrite.write(message)
                await IRCwrite.drain()
                print("Sent a PONG")

# Define execute function
async def main():
    print("Ready on Notification")
    await asyncio.gather(run(track[0]), run(track[1]), run(track[2]), run(track[3]), run(track[4])
                         , run(track[5]), run(track[6]), run(track[7]), run(track[8]))

# Start
if __name__ == '__main__':
    asyncio.run(main())