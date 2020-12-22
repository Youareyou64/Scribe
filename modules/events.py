from discord.ext.commands import Cog, command, CommandOnCooldown
import bot
from discord.ext import commands
from discord.ext.commands import CommandNotFound


class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(f"You're using that command too fast! Try again in {error.retry_after:,.2f} seconds.")
        elif isinstance(error, CommandNotFound):
            return
        else:
            print(error)
            await ctx.send(f"Command failed. Error message: `{error}`")

    @Cog.listener()
    async def on_disconnect(self, ctx):
        self.bot.nicknames.close()
        self.bot.muted_users.close()

    @Cog.listener()
    async def on_message(self, message) -> None:
        if message.author.bot:
            return
        bot_mentions = [f"<@{self.bot.user.id}>", f"<@!{self.bot.user.id}>"]
        if message.content in bot_mentions:
            await message.channel.send(f"Hello {message.author.mention}! My prefix is `s!`. Try `s!help` if you need help!")







def setup(bot):
    bot.add_cog(Events(bot))
