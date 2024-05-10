import asyncio
from flask_socketio import SocketIO, emit

class Chaser:
    def __init__(self, socketio, bpm=120, s_beat=None):
        self.current = 0
        self.s_beat = s_beat if s_beat is not None else []
        self.bpm = bpm
        self.task = None
        self.socketio = socketio

    async def start(self):
        print('-> chaser start')
        if self.task is not None:
            self.task.cancel()
        self.task = asyncio.create_task(self.movenext())

    async def stop(self):
        print('-> chaser stop')
        if self.task is not None:
            self.task.cancel()
            self.task = None

    async def reset(self):
        print('-> chaser reset')
        self.current = 0

    def setBpm(self, newBpm):
        self.bpm = newBpm
        if self.task is not None:
            asyncio.run(self.start())

    async def movenext(self):
        while True:
            print('-> chaser -> movenext')
            
            # Update the animation state here and send updates to the client
            self.current = (self.current + 1) % len(self.s_beat)
            self.socketio.emit('update', {'current': self.current})
            await asyncio.sleep(60.0/self.bpm)