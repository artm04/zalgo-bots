from threading import Thread
from abc import ABC, abstractmethod
import discord
from main import ZalgoText

zalgo = ZalgoText()


class UserInterface(Thread, ABC):

    def __init__(self, logger, zalgo_text: ZalgoText, token: str):
        super().__init__()
        self.logger = logger
        self.zalgo_text = zalgo_text
        self.token = token

    @abstractmethod
    def run(self):
        pass

    def polling(self):
        self.start()


class DiscordInterface(UserInterface):

    def __init__(self, logger, zalgo_text, token: str):
        super().__init__(logger, zalgo_text, token)
        self.client = discord.Client()

        @self.client.event
        async def on_ready():
            print('We have logged in as {0.user}'.format(self.client))

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            if message.content.startswith('/zalgo'):
                if message.content == "/zalgo":
                    await message.channel.send("Write text to be zalgofied after the /zalgo")
                else:
                    await message.channel.send(self.zalgo_text.zalgofy(message.content[6:]))

    def run(self):
        self.client.run(self.token)
