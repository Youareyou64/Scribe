from discord.ext.commands import Cog, command
from discord import utils
from discord.utils import get
import discord
from discord.ext import commands
from discord import Embed, Colour


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            help_embed = Embed(colour=Colour(0xff0000))
            help_embed.set_author(name="Scribe Help Categories:")
            help_embed.add_field(name="Support Server:",
                                 value="https://discord.gg/yq8qzhx", inline=False)
            help_embed.add_field(name="___________________________", value="⠀", inline=False)
            help_embed.add_field(name="general", value="General Commands", inline=False)
            help_embed.add_field(name="tts", value="TTS (Text to Speech) related commands", inline=False)
            help_embed.add_field(name="stt", value="STT (Speech to Text) related commands", inline=False)
            help_embed.add_field(name="moderation", value="Moderation related commands", inline=False)
            # help_embed.add_field(name="Errors", value="Get help with errors you may encounter")
            help_embed.add_field(name="To see commands in a category:", value="**Use `s!help <category>` with one of the above categories**")
            help_embed.set_footer(text="For help, feedback, bug reports, or suggestions, join our Discord Server! https://discord.gg/yq8qzhx")
            await ctx.send("", embed=help_embed)

    @help.command()
    async def general(self, ctx):
        embed = discord.Embed(title="General Commands", url="https://discord.gg/yq8qzhx",
                              description="Use s!help for all help categories", color=0x4b72e7)
        embed.add_field(name="info", value="General bot info", inline=False)
        embed.add_field(name="ping", value="Returns the bot's ping", inline=False)
        embed.add_field(name="stats", value="Approximate stats about the bot", inline=False)
        embed.add_field(name="contributors", value="See everyone who has helped with Scribe", inline=False)
        embed.add_field(name="invite", value="Invite the bot to your server", inline=False)
        embed.add_field(name="support", value="Get help with the bot, suggest features, etc. ", inline=False)
        embed.set_footer(text="Use s!help to see other help categories")
        await ctx.send(embed=embed)

    @help.command(aliases=['TTS', 'text to speech'])
    async def tts(self, ctx):
        embed = discord.Embed(title="TTS", url="https://discord.gg/yq8qzhx",
                              description="Use s!help for all help categories", color=0xaa71d1)
        embed.add_field(name="tts <message>", value="Have Scribe speak your message into a Voice Chat", inline=False)
        embed.add_field(name="join", value="Have Scribe join a Voice Chat", inline=False)
        embed.add_field(name="leave", value="Have Scribe leave a Voice Chat", inline=False)
        embed.add_field(name="nick <nickname>", value="Set a global nickname that is spoken before your TTS messages", inline=True)
        embed.set_footer(text="Use s!help to see other help categories")
        await ctx.send(embed=embed)

    @help.command()
    async def stt(self, ctx):
        embed = discord.Embed(title="STT", url="https://discord.gg/yq8qzhx",
                              description="Use s!help for all help categories", color=0x3fde4a)
        embed.add_field(name="record <time>",
                        value="Record audio from a voice chat and send into the channel where command was triggered." +
                              " Note that recordings over 30 seconds may not send due to Discord size limits. "
                              "Provide a time like 's!record 10s'.", inline=False)
        embed.add_field(name="stt", value="Coming soon!", inline=True)
        embed.set_footer(text="Use s!help to see other help categories")
        await ctx.send(embed=embed)

    @help.command(aliases=["mod"])
    async def moderation(self, ctx):
        embed = discord.Embed(title="Moderation", url="https://discord.gg/yq8qzhx",
                              description="Use s!help for all help categories", color=0xe4b944)
        embed.add_field(name="mute <@user | user_ID>", value="Prevent an user from using TTS", inline=False)
        embed.add_field(name="unmute <@user | user_ID>", value="Unmute an user", inline=False)
        embed.set_footer(text="Use s!help to see other help categories")
        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(Help(bot))
