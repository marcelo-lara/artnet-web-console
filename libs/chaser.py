import asyncio
from flask_socketio import SocketIO, emit

socketio = SocketIO(async_mode='eventlet')

class Chaser:
    def __init__(self, bpm=120, s_beat=None):
        self.current = 0
        self.s_beat = s_beat if s_beat is not None else []
        self.bpm = bpm
        self.task = None

    async def start(self):
        if self.task is not None:
            self.task.cancel()
        self.task = asyncio.create_task(self.movenext())

    async def stop(self):
        if self.task is not None:
            self.task.cancel()
            self.task = None

    def reset(self):
        self.current = 0

    def setBpm(self, newBpm):
        self.bpm = newBpm
        if self.task is not None:
            asyncio.run(self.start())

    async def movenext(self):
        while True:
            # Update the animation state here and send updates to the client
            self.current = (self.current + 1) % len(self.s_beat)
            socketio.emit('update', {'current': self.current})
            await asyncio.sleep(60.0/self.bpm)