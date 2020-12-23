from os import getenv
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        load_dotenv(verbose=True)
        self.default_prefix = ["s!", "<@!754137339760214097> ", "<@754137339760214097> "]
        # uncomment for dev prefixes
        # self.default_prefix = ["d!", "<@!791352105746300939> ", "<@791352105746300939> "]

    """
    @property
    def discord_token(self):
        return getenv("ALPHA_DISCORD_TOKEN")
    """
    @property
    def discord_token(self):
        return getenv("DISCORD_TOKEN")