from discord.ext.commands import Cog, command

import os
import asyncio
from io import BytesIO
from aiogtts import aiogTTS

from utils.queue_consumer import QueueConsumer
from utils.voice_message import VoiceMessage

class TTSModule(Cog):
    def __init__(self, bot):
        self.bot = bot

        self.queues = {}

    @command()
    async def tts(self, ctx):
        try:
            user_nick = self.bot.get_user_nick(ctx.author)
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            await self.queues[voice].put(VoiceMessage(" ".join(ctx.message.content.split(" ")[1:]), user_nick))

        except AttributeError:
            await ctx.send(":x: Error. Please have a moderator kick the bot from the voice channel and then send the join command again, or let bot connwction time out. ```AttributeError: Duplicated Voice Session upon reboot```")

    @command(aliases=["j", "joi"])
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
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.remove(file)
            print("Cache Cleared")
            await ctx.send(":white_check_mark: Cleared all saved TTS files")
        else:
            await ctx.send(":x: You do not have permission to take this action.")


    @command(aliases=["l", "lea"])
    async def leave(self, ctx):
        if ctx.message.author.voice:
            try:
                channel = ctx.message.author.voice.channel
                server = ctx.message.guild.voice_client
                await server.disconnect(force=True)
                await ctx.send(":ballot_box_with_check: I have left the channel")
            except:
                await ctx.send(":x: You must be in the voice channel that you'd like me to leave")
        else:
            await ctx.send(":x: You must be in the voice channel that you'd like me to leave!")

def setup(bot):
    bot.add_cog(TTSModule(bot))