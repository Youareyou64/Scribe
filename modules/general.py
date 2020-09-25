from discord import Embed, Colour
from discord.ext.commands import Cog, command
from discord.ext.commands import has_permissions
import shelve

class General(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def help(self, ctx, *, cmd: str='general'):
        print(cmd)
        if cmd.lower() == 'tts':
            await ctx.send("**TTS** | TTS can be used when you are in a voice chat and would like the bot to speak on your behalf. Simply type `s!tts [Your message here]`! Bot must be in VC to use.")
        elif cmd.lower() == 'stt':
            await ctx.send("STT Feature Coming Soon!")
        elif cmd.lower() == 'nick':
            await ctx.send("Use `s!nick [nickname]` to set a nickname that is spoken before any TTS message said on your behalf. Nicknames apply across all servers you are in.")
        elif cmd.lower() == 'me':
            await ctx.send("What's wrong? :/ *hugs*")
        elif cmd.lower() == 'mute':
            await ctx.send("Use to prevent an user from using the TTS command. Requires Mute Users server permission. Use unmute to unmute")
        elif cmd.lower() == 'general':
            print("general help triggered")
            help_embed = Embed(colour=Colour(0xff0000))
            help_embed.set_author(name="**Scribe Bot Commands**")
            help_embed.add_field(name="ping", value="Returns bot Ping", inline=False)
            help_embed.add_field(name="info", value="Displays info about the bot", inline=False)
            help_embed.add_field(name="contributors", value="Displays Bot Owner", inline=False)
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
        await ctx.send(f"Pong! **{round(self.bot.latency * 1000)}ms**")

    @command()
    async def nick(self, ctx, nickname: str):
        self.bot.nicknames[str(ctx.message.author.id)] = nickname
        print(f"{self.bot.user.id}'s nickname changed to {nickname}")
        await ctx.send(":ballot_box_with_check: Nickname changed to " + nickname)

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
        info_embed.add_field(name="Users", value=len(self.bot.users), inline=False)
        info_embed.add_field(name="Guilds", value=len(self.bot.guilds), inline=True)
        await ctx.send(embed=info_embed)

    @command()
    async def goodnight(self, ctx):
        await ctx.send(f"Goodnight {ctx.message.author.name}")

    @command()
    async def contributors(self, ctx):
        contrib_embed = Embed(colour=Colour(0xff0000))
        contrib_embed.set_author(name="Scribe Contributors")
        contrib_embed.add_field(name="Lead Dev", value="Youareyou#0513", inline=False)
        contrib_embed.add_field(name="Co Lead Dev", value="MvKal#6472", inline=False)
        contrib_embed.add_field(name="Contributor", value="OneUpPotato#1418", inline=False)
        contrib_embed.add_field(name="Hosting", value="deĉjo#7610 and the YACU", inline=False)
        contrib_embed.add_field(name="Special thanks to", value="Everyone else who helped out and provided support!", inline=False)
        await ctx.send(embed=contrib_embed)

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
