from threading import Thread
from abc import ABC, abstractmethod
import discord


class UserInterface(Thread, ABC):

    def __init__(self, logger, zalgo_text, token: str):
        super().__init__()
        self.logger = logger
        self.zalgo_text = zalgo_text
        self.token = token

    @abstractmethod
    def run(self):
        pass

    def polling(self):
        self.start()


class DiscordInterface(UserInterface, discord.client):

    def __init__(self, logger, zalgo_text, token: str):
        super().__init__(logger, zalgo_text, token)

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self.client))

    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.content.startswith('/zalgo'):
            await message.channel.send(message.content)

    def run(self):
        self.client.run(self.token)


dis_bot = DiscordInterface(None, None, "ODMwMTA1NTY0Nzk2ODEzMzc1.YHB2DQ.8IooalAlx0XyeDzU1NmnVijT5QQ")
dis_bot.start()
print("ass")





