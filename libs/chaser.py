import asyncio
from flask_socketio import SocketIO, emit

class Chaser:
    def __init__(self, socketio, bpm=120, s_beat=None):
        self.current = 0
        self.s_beat = s_beat if s_beat is not None else []
        self.bpm = bpm
        self.task = None
        self.socketio = socketio
        self.is_playing = False

    async def start(self):
        print('-> chaser start')
        if self.task is not None:
            self.task.cancel()
        self.is_playing = True

    async def stop(self):
        print('-> chaser stop')
        if self.task is not None:
            self.task.cancel()
            self.task = None
        self.is_playing = False

    async def reset(self):
        print('-> chaser reset')
        self.current = 0

    def setBpm(self, newBpm):
        self.bpm = newBpm
        self.socketio.emit('set_bpm', {'bpm': self.bpm})

    async def movenext(self):
        print('-> chaser -> movenext')
        
        # Update the animation state here and send updates to the client
        self.current = (self.current + 1) % len(self.s_beat)
        
        self.socketio.emit('update', {'current': self.current})
