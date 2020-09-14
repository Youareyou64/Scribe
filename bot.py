

import discord
from discord.ext import commands
import os
import asyncio
from io import BytesIO
from aiogtts import aiogTTS
from discord.utils import get
import shelve


client = commands.Bot(command_prefix='s!')
client.remove_command('help')

nicknames = shelve.open("nick_data")
# nicknames["435200177217732633"] = "Youareyou"

@client.event
async def on_ready():
    print('Bot is ready!')
    await client.change_presence(activity=discord.Game(name='type s!info'))
    nicknames = shelve.open("nick_data")


@client.command()
async def nick(ctx):
    global nnick
    nnickl = ctx.message.content
    nnick=nnickl.replace("s!nick", '')
    nicknames[str(ctx.message.author.id)] = nnick
    print(f"{client.user.id}'s nickname changed to {nnick}")
    await ctx.send(":ballot_box_with_check: Nickname changed to " + nnick)


@client.event
async def on_command_error(ctx, error):
    await ctx.send("Command failed error message `{0}` ".format(str(error)))

@client.event
async def on_disconnect():
    nicknames.close()


@client.command(pass_context=True)
async def tts(ctx):
    try:
        usernick = nicknames.get(str(ctx.message.author.id), "nonick")
        if usernick == "nonick":
            usernick == client.user.display_name
        # obtaining Mp3
        mess = str(ctx.message.content)
        mess = usernick + "says." + mess.replace("s!tts ", '')
        message_id = str(ctx.message.id)
        aiogtts=aiogTTS()
        io = BytesIO()
        await aiogtts.save(mess, "speech" + ".mp3", lang='en')
        await aiogtts.write_to_fp(mess, io, slow=False, lang='en')

        # playing mp3
        voice = get(client.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio("speech.mp3"), after=lambda e: print(f"Message has finished playing"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.2
    except:
        await ctx.send(":x: Error. Please have a moderator kick the bot from the voice channel and then send the join command again, or let bot connwction time out. ```AttributeError: Duplicated Voice Session upon reboot```")

@client.command()
async def help(ctx):
    helpembed = discord.Embed(
        colour=discord.Colour.red()
    )
    helpembed.set_author(name="**Scribe Bot Commands**")
    helpembed.add_field(name='ping', value='Returns bot Ping', inline=False)
    helpembed.add_field(name='info', value='Displays info about the bot', inline=False)
    helpembed.add_field(name='contributors', value='Displays Bot Owner', inline=False)
    helpembed.add_field(name='help', value='returns this message', inline=False)
    helpembed.add_field(name='join', value='Joins a VC that you are in', inline=False)
    helpembed.add_field(name='leave', value='leaves a VC that you are in', inline=False)
    helpembed.add_field(name='tts', value='Speaks your message into VC', inline=False)
    helpembed.add_field(name='nick <nickname>', value='Use command to set your TTS nickname, replace <nickname> with your desired nickname!', inline=False)

    await ctx.send(embed=helpembed)


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! **{round(client.latency * 1000)}ms**')




@client.command()
async def contributors(ctx):
    cont_embed = discord.Embed(
        colour=discord.Colour.red()
    )
    cont_embed.set_author(name="Scribe Contributors")
    cont_embed.add_field(name='Lead Dev', value='Youareyou#0513', inline=False)
    cont_embed.add_field(name='Special thanks to', value='The RPAN Mod Team (provided cute cat photos), all of my testers, and those who helped me troubleshoot', inline=False)

    await ctx.send(embed=cont_embed)


@client.command(pass_context=True, aliases=["j", "joi"])
async def join(ctx):
    try:
        global channel
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send(":white_check_mark: I have joined the voice channel!")
    except:
        await ctx.send(":x: Join failed, please ensure you are in a voice channel that the bot has access to!")


@client.command(pass_context=True)
async def clear(ctx):
    print(ctx.author.id)
    if str(ctx.author.id) == "435200177217732633":
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.remove(file)
        print("Cache Cleared")
        await ctx.send(":white_check_mark: Cleared all saved TTS files")
    else:
        await ctx.send(":x: You do not have permission to take this action.")


@client.command(pass_context=True, aliases=["l", "lea"])
async def leave(ctx):
    if ctx.message.author.voice:
        try:
            channel = ctx.message.author.voice.channel
            server = ctx.message.guild.voice_client
            await server.disconnect()
            await ctx.send(":ballot_box_with_check: I have left the channel")
        except:
            await ctx.send(":x: You must be in the voice channel that you'd like me to leave")
    else:
        await ctx.send(":x: You must be in the voice channel that you'd like me to leave!")


@client.command(pass_context=True)
async def info(ctx):
    info_embed = discord.Embed(
        title = 'Bot Info',
        colour= discord.Colour.blurple()
    )

    info_embed.set_footer(text='Contact @Youareyou#0513 with questions, feedback, or for help.')
    info_embed.set_author(name='Bot Information')
    info_embed.add_field(name='Scribe Bot', value='your friendly voice chat utility bot', inline=False)
    info_embed.add_field(name='Owner', value='@Youareyou#0513', inline=True)
    info_embed.add_field(name='Contributors', value='s!contributors', inline=False)
    info_embed.add_field(name='Help', value='s!help', inline=True)
    info_embed.add_field(name='Users', value=len(client.users), inline=False)
    info_embed.add_field(name='Guilds', value=len(client.guilds), inline=True)

    await ctx.send(embed=info_embed)

@client.command()
async def goodnight(ctx):
    await ctx.send(f'Goodnight {ctx.message.author.name}')


client.run(os.environ.get('ScribeToken'))
