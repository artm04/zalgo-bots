import json
from os.path import exists
from user_interfaces import DiscordInterface, TelegramInterface


class TokenReader:

    @staticmethod
    def get_tokens() -> dict:
        if not exists("tokens.json"):
            with open("tokens.json", "w", encoding='utf-8') as file:
                json.dump({"telegram": [], "discord": []}, file, ensure_ascii=False, indent=4)
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

    def __create_interfaces(self, logger, zalgo_text):
        for telegram_token in self.telegram_tokens:
            telegram_bot = TelegramInterface(logger, zalgo_text, telegram_token)
            telegram_bot.start()
        for discord_token in self.discord_tokens:
            discord_bot = DiscordInterface(logger, zalgo_text, discord_token)
            discord_bot.start()

    def run(self, token_reader: TokenReader, logger, zalgo_text):
        self.__read_tokens(token_reader)
        self.__create_interfaces(logger, zalgo_text)



