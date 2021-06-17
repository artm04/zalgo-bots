from zalgo_text.zalgo import zalgo


class ZalgoText:
    def zalgofy(self, text: str) -> str:
        if "[" in text and "]" in text:
            return self.parse_zalgo(text)
        return self.convert_to_zalgo(text)

    @staticmethod
    def convert_to_zalgo(text: str) -> str:
        """Тут он весь текст конвертирует"""
        return zalgo().zalgofy(text)

    def parse_zalgo(self, text: str) -> str:
        length = len(text)
        i = 0
        while i < length:
            if text[i] == "[":
                start = i
                while i < length:
                    if text[i] == "]":
                        text = text.replace(
                            text[start: i + 1], self.convert_to_zalgo(text[start + 1: i]))
                    i += 1
            i += 1
        return text
