from os import getenv
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        load_dotenv(verbose=True)
        self.default_prefix = "s!"

    @property
    def discord_token(self):
        return getenv("DISCORD_TOKEN")
