from discord.ext.commands import Cog, command, CommandOnCooldown
import bot
from discord.ext import commands



class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(f"You're using that command too fast! Try again in {error.retry_after:,.2f} seconds.")
        else:
            print(error)
            await ctx.send(f"Command failed. Error message: `{error}`")

    @Cog.listener()
    async def on_disconnect(self, ctx):
        self.bot.nicknames.close()
        self.bot.muted_users.close()


def setup(bot):
    bot.add_cog(Events(bot))
