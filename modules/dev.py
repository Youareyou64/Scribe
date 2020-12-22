from discord import Embed, Colour
from discord.ext.commands import Cog, command
import shelve
import discord
import psutil
from psutil import virtual_memory
from pygount import ProjectSummary, SourceAnalysis
from glob import glob
from discord.ext import commands

devs = [435200177217732633]

class Dev(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def echo(self, ctx, id, *, echowords: str):
        if ctx.message.author.id == 435200177217732633:  # put in id's in a list or replace it with one string
            sendchannel = self.bot.get_channel(int(id))
            await sendchannel.send(f"{echowords}")

    @command(aliases=["die", "close", "stop"])
    async def kill(self, ctx):
        if ctx.author.id == 435200177217732633:
            await ctx.send("Scribe out. `Connection closing...`")
            await ctx.bot.close()


def setup(bot):
    bot.add_cog(Dev(bot))