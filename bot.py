#YOU NEED TO INSTALL THE VOICE RECEIVE MODULE using: pip install -U "discord.py[voice] @ git+https://github.com/Gorialis/discord.py@voice-recv-mk3"

from discord import Game
from discord.utils import get
from discord.ext.commands import Bot

import shelve
from traceback import print_exc

from utils.settings import Settings


class ScribeBot(Bot):
    def __init__(self):
        # Load the bot's settings.
        self.settings = Settings()

        # Initiate the bot.
        super().__init__(
            command_prefix=self.settings.default_prefix,
            case_insensitive=True,
            activity=Game(name=f"Type {self.settings.default_prefix}info"),
        )

        # Remove the default help command.
        self.remove_command('help')

        # Load the nicknames shelve.
        self.nicknames = shelve.open("nick_data")



        # Load the modules.
        modules = ["general", "events", "tts", "stt"]
        for module in modules:
            try:
                self.load_extension(f"modules.{module}")
                print(f"MODULE: Loaded {module}.")
            except:
                print(f"MODULE: Error loading {module}.")
                print_exc()
                pass

        # Run the bot.
        self.run(self.settings.discord_token)

    async def on_ready(self):
        print('Bot is ready!')

        # Disconnect from any connected voice channels.
        for vcc in self.voice_clients:
            await vcc.disconnect(force=True)

    def get_user_nick(self, user):
        self.nicknames = shelve.open("nick_data")
        user_nick = self.nicknames.get(str(user.id), None)
        if user_nick == None:
            user_nick = user.display_name
        self.nicknames.close()
        return user_nick

