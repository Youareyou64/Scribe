from discord import Embed, Colour
from discord.ext.commands import Cog, command
import shelve
import discord
import psutil
from psutil import virtual_memory
from pygount import ProjectSummary, SourceAnalysis
from glob import glob
from discord.ext import commands


class General(Cog):
    def __init__(self, bot):
        self.bot = bot



    @command()
    async def oldhelp(self, ctx, *, cmd: str = 'general'):
        print(cmd)
        if cmd.lower() == 'tts':
            await ctx.send("**TTS** | TTS can be used when you are in a voice chat and would like the bot to speak on your behalf. Simply type `s!tts [Your message here]`! Bot must be in VC to use.")
        elif cmd.lower() == 'stt':
            await ctx.send("STT Feature Coming Soon! <:soontm:726858102271508571>")
        elif cmd.lower() == 'nick':
            await ctx.send("Use `s!nick [nickname]` to set a nickname that is spoken before any TTS message said on your behalf. Nicknames apply across all servers you are in.")
        elif cmd.lower() == 'me':
            await ctx.send("What's wrong? :/ *hugs*")
        elif cmd.lower() == 'mute':
            await ctx.send("Use to prevent an user from using the TTS command. Requires Mute Users server permission. Use unmute to unmute")
        elif cmd.lower() == 'record':
            await ctx.send("Records audio from a voice chat. Usage: `s!record <time>`. Example: `s!record 20s`")
        elif cmd.lower() == 'general':
            print("general help triggered")
            help_embed = Embed(colour=Colour(0xff0000))
            help_embed.set_author(name="Scribe Bot Commands")
            help_embed.add_field(name="For help, feedback, bug reports, or suggestions, join our Discord Server!", value="https://discord.gg/yq8qzhx", inline=False)
            help_embed.add_field(name="ping", value="Returns bot Ping", inline=False)
            help_embed.add_field(name="info", value="Displays info about the bot", inline=False)
            help_embed.add_field(name="contributors", value="Displays Bot Contributors", inline=False)
            help_embed.add_field(name="help", value="returns this message", inline=False)
            help_embed.add_field(name="join", value="Joins a VC that you are in", inline=False)
            help_embed.add_field(name="leave", value="leaves a VC that you are in", inline=False)
            help_embed.add_field(name="tts", value="Speaks your message into VC", inline=False)
            help_embed.add_field(name="mute", value="Mute an user from using TTS (use unmute to unmute)", inline=False)
            help_embed.add_field(name="nick", value="Set your TTS nickname that will be spoken before anything you say!", inline=False)
            help_embed.add_field(name="More Help", value="**Use `s!help [command]` for more help with a command!**")
            await ctx.send("", embed=help_embed)
        else:
            await ctx.send("""No advanced help found for that command. Here is a list of available advanced helps:
            tts
            stt
            nick
            mute""")

    @command()
    async def ping(self, ctx):
        async with ctx.typing():
            await ctx.send(f"Pong! **{round(self.bot.latency * 1000)}ms**")
            await ctx.send("Use `s!stats` for full bot stats")

    # @command(aliases=['bug', 'report', 'suggestion', 'contribute'])
    # async def support(self, ctx):
        # await ctx.send("To report a bug, get help, suggest a feature, or contribute to Scribe, join Scribe's Discord server! https://discord.gg/yq8qzhx")

    @command(aliases=["stats", "cpu", "ram", "system"])
    async def sys(self, ctx):

        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        memory = memory[1]

        memory = round(memory / 1024 / 1024)

        nmemory = virtual_memory().percent

        embed = discord.Embed(title="Scribe System Stats", description="Approximate statistics about Scribe's server",
                              color=0x2eff3c)
        embed.add_field(name="Ping", value=f"**{round(self.bot.latency * 1000)}ms**", inline=False)
        embed.add_field(name="CPU Usage", value=f"{cpu}%", inline=False)
        embed.add_field(name="RAM Usage", value=f"{nmemory}%", inline=True)

        embed.set_footer(text="s!help")
        await ctx.send(embed=embed)

    @command(aliases=["feedback", "support", "suggest", "suggestion", "bug", "report"])
    async def discord(self, ctx):
        embed = discord.Embed(title="Scribe's Discord Server", url="https://discord.gg/yq8qzhx",
                              description="Join Scribe's Discord server by clicking the link above to give feedback/suggestions, report bugs, get help, or contribute to Scribe!",
                              color=0x21cde4)
        embed.set_footer(text="For general help use s!help | https://discord.gg/yq8qzhx")
        await ctx.send(embed=embed)

    @command(aliases=["repo", "git", "repository"])
    async def github(self, ctx):
        embed = discord.Embed(title="Github Repo", url="https://github.com/Youareyou64/Scribe/",
                              description="Scribe's Github Repository", color=0xe5935d)
        embed.set_footer(text="Support Server: discord.gg/yq8qzhx")
        await ctx.send(embed=embed)

    @command()
    async def leave_server(self, ctx, srvr: int):
        if ctx.author.id == 435200177217732633:
            guild = self.bot.get_guild(srvr)
            await guild.leave()
        else:
            await ctx.send("Only bot devs can do this, if you'd like it to leave your server, use Discord's kick feature.")


    @command()
    async def privacy(self, ctx):
        privacyembed = Embed(colour=Colour(0xff0000))
        privacyembed.set_author(name="**Scribe Privacy Policy**")
        privacyembed.add_field(name="Scribe's Privacy policy can be viewed here", value="https://pastebin.com/FbXLrQTi")
        await ctx.send("", embed=privacyembed)

    @command()
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def nick(self, ctx, nickname: str):
        self.bot.nicknames = shelve.open("nick_data")
        self.bot.nicknames[str(ctx.message.author.id)] = nickname
        print(f"{self.bot.user.id}'s nickname changed to {nickname}")
        await ctx.send(":ballot_box_with_check: Nickname changed to " + nickname)
        self.bot.nicknames.close()

    @command()
    async def invite(self, ctx):
        await ctx.send("As I am still in a development phase, please DM <@!435200177217732633> if you're interested in getting me in your server.")

    @command()
    async def info(self, ctx):
        info_embed = Embed(title="Bot Info", colour=Colour(0x7289DA))
        info_embed.set_footer(text="Contact @Youareyou#0513 with questions, feedback, or for help.")
        info_embed.set_author(name="Bot Information")
        info_embed.add_field(name="Scribe Bot", value="your friendly voice chat utility bot", inline=False)
        info_embed.add_field(name="Owner", value="@Youareyou#0513", inline=True)
        info_embed.add_field(name="Contributors", value="s!contributors", inline=False)
        info_embed.add_field(name="Help", value="s!help", inline=True)
        info_embed.add_field(name="Users", value=str(len(self.bot.users)), inline=False)
        info_embed.add_field(name="Guilds", value=str(len(self.bot.guilds)), inline=True)
        await ctx.send(embed=info_embed)

    @command()
    async def goodnight(self, ctx):
        await ctx.send(f"Goodnight {ctx.message.author.name}")

    @command()
    async def work(self, ctx):
        await ctx.send("It's your job to make me")

    @command()
    async def contributors(self, ctx):
        embed = discord.Embed(title="Contributors", description="Everyone who has helped with Scribe", color=0x54add9)
        embed.add_field(name="Lead Dev", value="Youareyou#0513", inline=False)
        embed.add_field(name="Code Contributors", value="SamKal, OneUpPotato", inline=False)
        embed.add_field(name="Other Contributors", value="JayRy27, CZMG, ", inline=False)
        await ctx.send(embed=embed)

    @command()
    async def mute(self, ctx, *, user: str):
        if ctx.author.guild_permissions.mute_members:
            muted_users = shelve.open("muted_users")
            muted_users[user] = True
            print(f"{user} has been muted")
            await ctx.send(f"{user} has been muted")
        else:
            await ctx.send(f":x: You are unable to mute {user} because you do not have the Mute Users server permission.")

    @command()
    async def unmute(self, ctx, *, user: str):
        if ctx.author.guild_permissions.mute_members:
            muted_users = shelve.open("muted_users")
            muted_users[user] = False
            print(f"{user} has been unmuted")
            await ctx.send(f"{user} has been unmuted")
        else:
            await ctx.send(f":x: You are unable to unmute {user} because you do not have the Mute Users server permission.")




def setup(bot):
    bot.add_cog(General(bot))
