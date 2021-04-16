from threading import Thread
from abc import ABC, abstractmethod
import discord
import telebot
from zalgo import ZalgoText


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

            elif "private" in message.channel.type:  # DM. message.channel.type == "private" doesn't work
                await message.channel.send(self.zalgo_text.zalgofy(message.content))

    def run(self):
        self.client.run(self.token)


class TelegramInterface(UserInterface):

    def __init__(self, logger, zalgo_text, token: str):
        super().__init__(logger, zalgo_text, token)
        self.client = telebot.TeleBot(token)

        @self.client.message_handler(commands=['zalgo'])
        def zalgofy_command(message: telebot.types.Message):
            if message.text == "/zalgo":
                self.client.reply_to(message, "Write text to be zalgofied after the /zalgo")
            else:
                source = telebot.util.extract_arguments(message.text)
                self.client.reply_to(message, self.zalgo_text.zalgofy(source))

        @self.client.message_handler(func=lambda message: message.chat.type == 'private')
        def zalgofy_pm(message: telebot.types.Message):
            self.client.reply_to(message, self.zalgo_text.zalgofy(message.text))

        @self.client.inline_handler(func=lambda query: len(query.query) > 0)
        def zalgofy_inline(query: telebot.types.InlineQuery):
            zalgofied_text = self.zalgo_text.zalgofy(query.query)
            answer = telebot.types.InlineQueryResultArticle('1', zalgofied_text,
                                                            telebot.types.InputTextMessageContent(zalgofied_text))
            self.client.answer_inline_query(query.id, [answer])

    def run(self):
        self.client.infinity_polling()
