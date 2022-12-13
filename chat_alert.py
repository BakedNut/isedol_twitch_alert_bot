import connect
import socket
import time
from json import loads

print('ISEDOL CHAT ALERT START')

# Connect Telegram
TG = connect.ConnectTG("private") # Input "private" or "public"
bot = TG.bot

# Channels
tracking_id = ("vo_ine", "jingburger", "lilpaaaaaa", "cotton__123", "gosegugosegu", "viichan6", "woowakgood", "chunyangkr", "111roentgenium")
isedol_id = ("vo_ine", "jingburger", "lilpaaaaaa", "cotton__123", "gosegugosegu", "viichan6", "woowakgood")
isedol_kr = {"vo_ine":"아이네 ⚪️", "jingburger":"징버거 🟡", "lilpaaaaaa":"릴파 🔵", "cotton__123":"주르르 🟣"
             , "gosegugosegu":"고세구 🦠", "viichan6":"비챤 🟢", "woowakgood":"우왁굳 🐵", "chunyangkr":"천양 🐡", "111roentgenium":"뢴트게늄 ☢"}

selID = tracking_id[0] #Ine

def run(ID):
    SERVER = "irc.twitch.tv"
    PORT = 6667
    PASSWORD = connect.Autho.OAuth  # This needs to be an OAuth token
    USERNAME = ID # Connect This Channel ID
    CHANNEL = USERNAME
    Connecting = True
    IRC = socket.socket()
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
                    print(f"{ID} Connected")
                    Connecting = False
        except:
            print(f'{ID} Connect Fail.. Retry')
            IRC = socket.socket()
            IRC.connect((SERVER, PORT))
            IRC.send(
                (
                    "PASS " + PASSWORD + "\n" +
                    "NICK " + USERNAME + "\n" +
                    "JOIN #" + CHANNEL + "\n"
                )
                .encode()
            )
                
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
                if user in isedol_id:
                    if user == USERNAME:
                        bot.sendMessage(chat_id=TG.chat_id, text= isedol_kr[user] + ":\n" + message)
                    else:
                        bot.sendMessage(chat_id=TG.chat_id, text= isedol_kr[user] + " → " + isedol_kr[USERNAME] + ":\n" + message)
            elif "PING" in line:
                print("Received a PING")
                message = "PONG tmi.twitch.tv\r\n".encode()
                IRC.send(message)
                print("Sent a PONG")

if '__name__' == '__main__':
    run(selID)