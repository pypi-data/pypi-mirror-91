from irc.bot import SingleServerIRCBot
from irc.client import ServerConnection, Event

from .models import TwitchTags


class BitBitBot(SingleServerIRCBot):
    SERVER = 'irc.chat.twitch.tv'
    PORT = 6667

    def __init__(self, username: str, token: str, channel: str):
        self.username = username
        self.channel = '#' + channel

        super().__init__(
            server_list=[
                (self.SERVER, self.PORT, token),
            ],
            nickname=self.username,
            realname=self.username,
        )

    def on_welcome(self, conn: ServerConnection, event: Event):
        conn.cap('REQ', ':twitch.tv/membership')
        conn.cap('REQ', ':twitch.tv/tags')
        conn.cap('REQ', ':twitch.tv/commands')
        conn.join(self.channel)

    def on_pubmsg(self, conn: ServerConnection, event: Event):
        msg = event.arguments[0]
        tags = TwitchTags.parse_obj({
            tag['key'].replace('-', '_'): tag['value']
            for tag in event.tags
        })

        print(f'{tags.display_name}: {msg}')
