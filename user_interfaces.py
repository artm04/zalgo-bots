from abc import ABC, abstractmethod
import discord
import aiogram
from zalgo import ZalgoText


class UserInterface(ABC):

    def __init__(self, logger, zalgo_text: ZalgoText, token: str):
        super().__init__()
        self.logger = logger
        self.zalgo_text = zalgo_text
        self.token = token

    @abstractmethod
    def run(self):
        pass


class DiscordInterface(UserInterface):

    def __init__(self, logger, zalgo_text, token: str):
        super().__init__(logger, zalgo_text, token)
        self.client = discord.Client()

        @self.client.event
        async def on_ready():
            self.logger.log_to_console_and_file('We have logged in as {0.user}'.format(self.client))

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            if message.content.startswith('/zalgo'):
                self.logger.log_to_console_and_file("Discord: /zalgo")
                if message.content == "/zalgo":
                    await message.channel.send("Write text to be zalgofied after the /zalgo")
                else:
                    await message.channel.send(self.zalgo_text.zalgofy(message.content[6:]))

            elif "private" in message.channel.type:  # DM. message.channel.type == "private" doesn't work
                self.logger.log_to_console_and_file("Discord: PM's")
                await message.channel.send(self.zalgo_text.zalgofy(message.content))

    async def run(self):
        await self.client.start(self.token)


class TelegramInterface(UserInterface):

    def __init__(self, logger, zalgo_text, token: str):
        super().__init__(logger, zalgo_text, token)
        self.client = aiogram.Bot(token)
        self.dp = aiogram.Dispatcher(self.client)

        @self.dp.message_handler(commands=['zalgo'])
        async def zalgofy(message: aiogram.types.Message):
            self.logger.log_to_console_and_file("Telegram: /zalgo")

            source = message.get_args()
            if source:
                await message.answer(self.zalgo_text.zalgofy(source))
            else:
                await message.answer("Write text to be zalgofied after the /zalgo")

        @self.dp.message_handler(lambda message: message.chat.type == 'private')
        async def zalgofy_pm(message: aiogram.types.Message):
            self.logger.log_to_console_and_file("Telegram: PM's")
            await message.answer(self.zalgo_text.zalgofy(message.text))

        @self.dp.inline_handler(lambda query: len(query.query) > 0)
        async def zalgofy_inline(query: aiogram.types.InlineQuery):
            self.logger.log_to_console_and_file("Telegram: Inline")
            zalgofied_text = self.zalgo_text.zalgofy(query.query)
            answer = aiogram.types.InlineQueryResultArticle(id='1', title=zalgofied_text,
                                                            input_message_content=aiogram.types.InputTextMessageContent(
                                                                zalgofied_text))
            await query.answer([answer])

    async def run(self):
        await self.dp.start_polling()
