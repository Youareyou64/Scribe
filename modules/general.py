from discord import Embed, Colour
from discord.ext.commands import Cog, command

class General(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def help(self, ctx):
        help_embed = Embed(colour=Colour(0xff0000))
        help_embed.set_author(name="**Scribe Bot Commands**")
        help_embed.add_field(name="ping", value="Returns bot Ping", inline=False)
        help_embed.add_field(name="info", value="Displays info about the bot", inline=False)
        help_embed.add_field(name="contributors", value="Displays Bot Owner", inline=False)
        help_embed.add_field(name="help", value="returns this message", inline=False)
        help_embed.add_field(name="join", value="Joins a VC that you are in", inline=False)
        help_embed.add_field(name="leave", value="leaves a VC that you are in", inline=False)
        help_embed.add_field(name="tts", value="Speaks your message into VC", inline=False)
        help_embed.add_field(name="nick <nickname>", value="Use command to set your TTS nickname, replace <nickname> with your desired nickname!", inline=False)
        await ctx.send("", embed=help_embed)

    @command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! **{round(client.latency * 1000)}ms**")

    @command()
    async def nick(self, ctx, nickname: str):
        self.bot.nicknames[str(ctx.message.author.id)] = nickname
        print(f"{client.user.id}'s nickname changed to {nnick}")
        await ctx.send(":ballot_box_with_check: Nickname changed to " + nnick)

    @command()
    async def info(self, ctx):
        info_embed = Embed(title="Bot Info", colour=Colour(0x7289DA))
        info_embed.set_footer(text="Contact @Youareyou#0513 with questions, feedback, or for help.")
        info_embed.set_author(name="Bot Information")
        info_embed.add_field(name="Scribe Bot", value="your friendly voice chat utility bot", inline=False)
        info_embed.add_field(name="Owner", value="@Youareyou#0513", inline=True)
        info_embed.add_field(name="Contributors", value="s!contributors", inline=False)
        info_embed.add_field(name="Help", value="s!help", inline=True)
        info_embed.add_field(name="Users", value=len(client.users), inline=False)
        info_embed.add_field(name="Guilds", value=len(client.guilds), inline=True)
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
        contrib_embed.add_field(name="Special thanks to", value="The RPAN Mod Team (provided cute cat photos), all of my testers, and those who helped me troubleshoot", inline=False)
        await ctx.send(embed=contrib_embed)

def setup(bot):
    bot.add_cog(General(bot))
