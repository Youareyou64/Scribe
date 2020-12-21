from discord.ext.commands import Cog, command
from discord import utils
from discord.utils import get
import discord
from discord.ext import commands


import shelve
import os
import asyncio
import pathlib
from pathlib import Path
discord.opus.load_opus(str(Path.cwd() / "waves\libopus.dll"))

from utils.queue_consumer import QueueConsumer
from utils.voice_message import VoiceMessage

class TTSModule(Cog):
    def __init__(self, bot):
        self.bot = bot

        self.queues = {}

    @command()
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def tts(self, ctx):

        muted_users = shelve.open("muted_users")
        is_muted = muted_users.get("<@!" + (str(ctx.author.id) + ">"), default=False)
        if is_muted == False:
            try:
                await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
                user_nick = self.bot.get_user_nick(ctx.author)
                voice = get(self.bot.voice_clients, guild=ctx.guild)
                await self.queues[voice].put(VoiceMessage(" ".join(ctx.message.content.split(" ")[1:]), user_nick))

            except AttributeError:
                await ctx.send(":x: Error. Please have a moderator kick the bot from the voice channel and then send the join command again, or let bot connection time out. ```AttributeError: Duplicated Voice Session upon reboot```")
            except KeyError:
                await ctx.send(":x: Error. I must be in a voice channel to use this command.")
        else:
            print("Failed to TTS, user is muted")
            await ctx.send("TTS Failed. User has been banned from using TTS. Use s!unmute to unmute.")



    @command(aliases=["j", "joi"])
    @commands.cooldown(2, 20, commands.BucketType.guild)
    async def join(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            vclient = await channel.connect()

            queue = asyncio.queues.Queue()
            self.queues[vclient] = queue

            asyncio.create_task(QueueConsumer(queue, vclient).start_consuming())
            await ctx.send(":white_check_mark: I have joined the voice channel!")
        except:
            await ctx.send(":x: Join failed, please ensure you are in a voice channel that the bot has access to!")

    @command()
    async def clear(self, ctx):
        if ctx.author.id == 435200177217732633:
            for file in os.listdir("./messages"):
                if file.endswith(".mp3"):
                    os.remove(file)
            print("Cache Cleared")
            await ctx.send(":white_check_mark: Cleared all saved TTS files")
        else:
            await ctx.send(":x: You do not have permission to take this action.")


    @command(aliases=["l", "lea"])
    @commands.cooldown(3, 15, commands.BucketType.user)
    async def leave(self, ctx):
        if ctx.message.author.voice:
            try:
                channel = ctx.message.author.voice.channel
                server = ctx.message.guild.voice_client
                await server.disconnect(force=True)
                await ctx.send(":ballot_box_with_check: I have left the channel")
            except:
                await ctx.send(":x: There was an error leaving the VC")
        else:
            vc = ctx.message.guild.voice_client
            await vc.disconnect()
            await ctx.send(':ballot_box_with_check: I have left the channel')

    


def setup(bot):
    bot.add_cog(TTSModule(bot))
