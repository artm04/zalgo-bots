import asyncio
import json
from os.path import exists
from typing import List
from user_interfaces import DiscordInterface, TelegramInterface, UserInterface


class TokenReader:

    @staticmethod
    def get_tokens() -> dict:
        if not exists("tokens.json"):
            with open("tokens.json", "w", encoding='utf-8') as file:
                json.dump({"telegram": [], "discord": []},
                          file, ensure_ascii=False, indent=4)
        with open("tokens.json", "r", encoding='utf-8') as file:
            tokens_dict = json.load(file)
        if not tokens_dict["telegram"] and not tokens_dict["discord"]:
            print("tokens.json have to look like:", "{'telegram': ['token_1', 'token_2', ...],",
                  "'discord': ['token_1', 'token_2', ...]}", sep="\n")
        return tokens_dict


class InterfacesFactory:

    def __init__(self):
        self.telegram_tokens = []
        self.discord_tokens = []
        self.logger = None

    def __read_tokens(self, token_reader: TokenReader):
        tokens = token_reader.get_tokens()
        self.telegram_tokens = tokens["telegram"]
        self.discord_tokens = tokens["discord"]

    def __create_interfaces(self, logger, zalgo_text) -> List[UserInterface]:
        bots = []
        for telegram_token in self.telegram_tokens:
            bots.append(TelegramInterface(logger, zalgo_text, telegram_token))
        for discord_token in self.discord_tokens:
            bots.append(DiscordInterface(logger, zalgo_text, discord_token))
        return bots

    def __start_interfaces(self, logger, zalgo_text):
        bots = self.__create_interfaces(logger, zalgo_text)
        loop = asyncio.get_event_loop()
        for bot in bots:
            loop.create_task(bot.run())
        loop.run_forever()

    def run(self, token_reader: TokenReader, logger, zalgo_text):
        self.__read_tokens(token_reader)
        self.__start_interfaces(logger, zalgo_text)
