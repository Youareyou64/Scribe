from discord.ext.commands import Cog, command
import bot




class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)
        await ctx.send(f"Command failed error message `{error}`")

    @Cog.listener()
    async def on_disconnect(self, ctx):
        self.bot.nicknames.close()
        self.bot.muted_users.close()


def setup(bot):
    bot.add_cog(Events(bot))
