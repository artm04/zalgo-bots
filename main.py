from interfaces_factory import TokenReader, InterfacesFactory
from logger import Logger
from zalgo import ZalgoText

if __name__ == "__main__":
    token_reader = TokenReader()
    factory = InterfacesFactory()

    logger = Logger()
    zalgo = ZalgoText()

    factory.run(token_reader, logger, zalgo)
