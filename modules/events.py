from discord.ext.commands import Cog, command

class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)
        await ctx.send(f"Command failed error message `{error}`")

    @Cog.listener()
    async def on_disconnect(self):
        self.bot.nicknames.close()

def setup(bot):
    bot.add_cog(Events(bot))
