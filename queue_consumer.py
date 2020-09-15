import asyncio
class QueueConsumer:
    def __init__(self, queue, voice_client):
        self.queue = queue
        self.voice = voice_client

    async def start_consuming(self):
        while True:
            message = await self.queue.get()
            await message.speak(self.voice)
            await asyncio.sleep(1)