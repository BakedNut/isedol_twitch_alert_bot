import asyncio
import re
import traceback
from collections import namedtuple

import aiohttp

USERNAME = ""
PASSWORD = ""

NAMED = (
    "vo_ine",
    "jingburger",
    "lilpaaaaaa",
    "cotton__123",
    "gosegugosegu",
    "viichan6",
    "woowakgood",
    "chunyangkr",
    "111roentgenium",
)


IRC_REGEX = re.compile(
    r"^(@(?P<tags>[^ ]*) )?(:(?P<source>[^ ]+) +)?(?P<command>[^ ]+)( *(?P<argument> .+))?"
)


class TwitchIRC:
    HOST = "wss://irc-ws.chat.twitch.tv"
    IGNORE_USERS = ["nightbot", "ssakdook", "streamelements"]

    Event = namedtuple("Event", ["source", "command", "argument", "tags"])

    def __init__(self, username, auth, channels, callback, callback_args={}):
        self.username = username
        self.auth = auth
        self.channels = channels

        self.callback = callback
        self.callback_args = callback_args

        self.session: aiohttp.ClientSession = None
        self.connection: aiohttp.ClientWebSocketResponse = None

    async def start(self):
        await self.connect()

        while True:
            try:
                if self.connection.closed:
                    await self.connect()

                try:
                    msg = await self.connection.receive(timeout=10)
                    event = self._parse_message(msg.data)

                    if event.command == "PING":
                        await self.connection.send_str(f"PONG {event.argument}")
                    elif hasattr(self, f"on_{event.command.lower()}"):
                        await getattr(self, f"on_{event.command.lower()}")(event)

                except asyncio.TimeoutError:
                    pass
            except:
                await self.session.post(
                    "https://discord.com/api/webhooks/986945409882652692/_-6GV-eiW3XXV9wvKNcmEmvLGXDq4AjSNKba0W1IhuPRFLQSrGjgGYoEelgpiQH9obP9",
                    data={
                        "content": "**TwitchIRC while**\n```\n"
                        + traceback.format_exc()
                        + "```"
                    },
                )

    async def connect(self):
        self.session = aiohttp.ClientSession()
        self.connection = await self.session.ws_connect(self.HOST)

        await self.connection.send_str("CAP REQ :twitch.tv/tags twitch.tv/commands")

        await self.connection.send_str(f"PASS {self.auth}")
        await self.connection.send_str(f"NICK {self.username}")

        for channel in self.channels:
            await self.connection.send_str(f"JOIN #{channel}")

    def _parse_message(self, message: str) -> Event:
        group = IRC_REGEX.match(message).group

        source = group("source")
        command = group("command")
        argument = group("argument")
        tags = group("tags")

        source = source.strip() if source else None
        command = command.strip() if command else None
        argument = argument.strip() if argument else None
        tags = (
            {tag.split("=")[0]: tag.split("=")[1] for tag in tags.strip().split(";")}
            if tags
            else {}
        )

        return self.Event(source, command, argument, tags)

    async def on_privmsg(self, event: Event):
        channel = event.argument.split(" :", 1)[0][1:]
        user = event.source.split("!", 1)[0]
        content = event.argument.split(" :", 1)[1]

        await self.request(channel, user, content)

    async def on_usernotice(self, event: Event):
        argument = event.argument.split(" :", 1)

        channel = argument[0][1:]
        user = event.source.split("!", 1)[0]

        month = event.tags.get("msg-param-cumulative-months")
        msg_type = event.tags.get("msg-id")

        if msg_type == "resub" and month:
            content = f"[{month}개월 구독]"

            if len(argument) > 1:
                content += " " + argument[1]

            await self.request(channel, user, content)

    async def request(self, channel, user, content):
        if user not in NAMED:
            return

        await self.callback(
            channel=channel,
            user=user,
            content=content,
            **self.callback_args,
        )


async def irc_callback(channel, user, content):
    # TODO
    ...


async def main():
    irc = TwitchIRC(
        USERNAME,
        PASSWORD,
        NAMED,
        irc_callback,
        callback_args={},
    )

    await irc.start()


asyncio.run(main())
