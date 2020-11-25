from discord.ext.commands import Cog, command
from discord.ext import commands
from discord import utils
from discord.utils import get
import parsedatetime as pdt
import datetime
from dateutil.relativedelta import relativedelta
import re
import discord

import pathlib
import shelve
import os
import asyncio

devs = [435200177217732633, 554807126174990349, 430453791889031168, 564751291100823552, 332935845004705793]

class ShortTime:
    compiled = re.compile("""(?:(?P<years>[0-9])(?:years?|y))?             # e.g. 2y
                             (?:(?P<months>[0-9]{1,2})(?:months?|mo))?     # e.g. 2months
                             (?:(?P<weeks>[0-9]{1,4})(?:weeks?|w))?        # e.g. 10w
                             (?:(?P<days>[0-9]{1,5})(?:days?|d))?          # e.g. 14d
                             (?:(?P<hours>[0-9]{1,5})(?:hours?|h))?        # e.g. 12h
                             (?:(?P<minutes>[0-9]{1,5})(?:minutes?|m))?    # e.g. 10m
                             (?:(?P<seconds>[0-9]{1,5})(?:seconds?|s))?    # e.g. 15s
                          """, re.VERBOSE)

    def __init__(self, argument, *, now=None):
        match = self.compiled.fullmatch(argument)
        if match is None or not match.group(0):
            raise commands.BadArgument('invalid time provided')

        data = { k: int(v) for k, v in match.groupdict(default=0).items() }
        now = now or datetime.datetime.utcnow()
        self.dt = now + relativedelta(**data)

    @classmethod
    async def convert(cls, ctx, argument):
        return cls(argument, now=ctx.message.created_at)


class HumanTime:
    calendar = pdt.Calendar(version=pdt.VERSION_CONTEXT_STYLE)

    def __init__(self, argument, *, now=None):
        now = now or datetime.datetime.utcnow()
        dt, status = self.calendar.parseDT(argument, sourceTime=now)
        if not status.hasDateOrTime:
            raise commands.BadArgument('invalid time provided, try e.g. "tomorrow" or "3 days"')

        if not status.hasTime:
            # replace it with the current time
            dt = dt.replace(hour=now.hour, minute=now.minute, second=now.second, microsecond=now.microsecond)

        self.dt = dt
        self._past = dt < now

    @classmethod
    async def convert(cls, ctx, argument):
        return cls(argument, now=ctx.message.created_at)


class Time(HumanTime):
    def __init__(self, argument, *, now=None):
        try:
            o = ShortTime(argument, now=now)
        except Exception as e:
            super().__init__(argument)
        else:
            self.dt = o.dt
            self._past = False


class FutureTime(Time):
    def __init__(self, argument, *, now=None):
        super().__init__(argument, now=now)

        if self._past:
            raise commands.BadArgument('this time is in the past')


class UserFriendlyTime(commands.Converter):
    """That way quotes aren't absolutely necessary."""
    def __init__(self, converter=None, *, default=None):
        if isinstance(converter, type) and issubclass(converter, commands.Converter):
            converter = converter()

        if converter is not None and not isinstance(converter, commands.Converter):
            raise TypeError('commands.Converter subclass necessary.')

        self.converter = converter
        self.default = default


class STTModule(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def record(self, ctx: commands.Context, time: FutureTime):
        global rnumber
        rnumber = 0
        try:
            await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
            waves_folder = pathlib.Path("./waves")
            waves_file_format = str(ctx.message.id) + '.wav'
            if not ctx.voice_client:
                channel = ctx.message.author.voice.channel
                await channel.connect()
            wave_file = waves_folder / str(waves_file_format)
            wave_file.touch()
            fp = wave_file.open('rb')
            ctx.voice_client.listen(discord.WaveSink(str(wave_file)))
            await discord.utils.sleep_until(time.dt)
            ctx.voice_client.stop_listening()

            # print(discord.File(fp, filename='record.wav'))
            await ctx.send("Recording being sent. Please wait!")
            await ctx.send('Here\'s your recording file.', file=discord.File(fp, filename=str(wave_file.name)))
            fp.close()
            rnumber += 1
        except:
            waves_folder = pathlib.Path("./waves")
            waves_file_format = str(ctx.message.id) + '.wav'
            wave_file = waves_folder / str(waves_file_format)
            fp = wave_file.open('rb')
            fp.close()
            await ctx.send('Your recording could not be sent, likely because it is too large.')

        print('after fp close')
        # file clearing

        print("waiting to del wavs")
        await asyncio.sleep(5)
        files_in_directory = os.listdir("./waves")
        filtered_files = [file for file in files_in_directory if file.endswith(".wav")]
        for file in filtered_files:
            path_to_file = os.path.join("./waves", file)
            os.remove(path_to_file)
        print('wavs cleared')

    @command()
    async def clearwav(self, ctx):
        if ctx.author.id in devs:
            files_in_directory = os.listdir("./waves")
            filtered_files = [file for file in files_in_directory if file.endswith(".wav")]
            for file in filtered_files:
                path_to_file = os.path.join("./waves", file)

                os.remove(path_to_file)
            print('wavs cleared')
            await ctx.send('Wav files cleared (use `clearmsg` to clear tts mp3s.')
        else:
            await ctx.send('Only devs can do this')

    @command()
    async def clearmsg(self, ctx):
        if ctx.author.id in devs:
            files_in_directory = os.listdir("./messages")
            filtered_files = [file for file in files_in_directory if file.endswith(".mp3")]
            for file in filtered_files:
                path_to_file = os.path.join("./messages", file)

                os.remove(path_to_file)
            print('mp3s cleared')
            await ctx.send('mp3 tts files cleared')
        else:
            await ctx.send('Only devs can do this')

def setup(bot):
    bot.add_cog(STTModule(bot))