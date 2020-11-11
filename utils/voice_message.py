import hashlib
import os
import asyncio
import discord


gtts_syncmode = True


def syncgen(contents, filename):
    import gtts
    print("Generating message...")
    gtts.gTTS(contents, lang="en").save(filename)
    print("Message generated and saved!")





async def generate_soundfile(contents, filename):
    coro = None
    print("Generating {0}: {1}".format(filename, contents))
    if gtts_syncmode:
        async def wrapper(contents, filename):
            return await asyncio.get_running_loop().run_in_executor(None, syncgen, contents, filename)
        coro = wrapper(contents, filename)
    else:
        import aiogtts
        coro = aiogtts.aiogTTS().save(contents, filename, lang='en')
    return coro


class VoiceMessage:
    def __init__(self, message, nickname_of_speaker):
        self.message = message
        self.author_nick = nickname_of_speaker
        self.spoken = False
        self.nickspoken = False

        self.nickhash = hashlib.md5(self.author_nick.encode()).hexdigest()
        self.nickgen = asyncio.create_task(self.nick_generator())

        self.msghash = hashlib.md5(self.message.encode()).hexdigest()
        self.message_gen = asyncio.create_task(self.message_generator())
        print("Message created, voice generating...")

    async def nick_generator(self):
        cache_filename = self.nickhash + ".mp3"
        if cache_filename not in os.listdir("nicknames_cache"):
            await asyncio.create_task(await generate_soundfile("{0} says.".format(self.author_nick), "nicknames_cache/" + cache_filename))
            print("nickname generated")
        else:
            print("nickname was cached")

    async def message_generator(self):
        return asyncio.create_task(await generate_soundfile(self.message, "messages/{0}.mp3".format(self.msghash)))

    async def speak(self, voice_client):
        print("Speaking {0}: {1}".format(self.author_nick, self.message))
        await self.nickgen
        voice_client.play(discord.FFmpegPCMAudio("nicknames_cache/{0}.mp3".format(self.nickhash)),
                        after=self.nick_said)
        print("nickname speaking, waiting for it to finish speaking")
        while not self.nickspoken:
            await asyncio.sleep(0.5)
            print("...")
        print("nick said!")
        await self.message_gen
        save_timer = 0
        while not ("messages/{0}.mp3".format(self.msghash)) in os.listdir("messages") and save_timer < 25:
            await asyncio.sleep(0.1)
            print('waiting for message to save' + str(save_timer))
            save_timer += 1
        print('im here')
        voice_client.play(discord.FFmpegPCMAudio("messages/{0}.mp3".format(self.msghash)), after=self.cleanup)
        while not self.spoken:
            await asyncio.sleep(1)

    def cleanup(self, *args):
        try:
            os.remove("messages/{0}.mp3".format(self.msghash))
        except FileNotFoundError:
            pass
        print("Message spoken")
        self.spoken = True

    def nick_said(self, *args):
        self.nickspoken = True
        print("Nick said")
