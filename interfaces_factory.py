import json
from os.path import exists


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


token_reader = TokenReader()
token_reader.get_tokens()
