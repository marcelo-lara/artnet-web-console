from libs.fixtures.fixture import Fixture
CHANNELS = [
    'X', 
    'Xx', 
    'Y', 
    'Yy', 
    'speed', 
    'dimmer', 
    'shutter', 
    'color', 
    'gobo', 
    'autoplay', 
    'autorun', 
    'reset'
]

class Head(Fixture):
    def __init__(self, start_channel, name, **kwargs):
        super().__init__(start_channel, name, channel_names=CHANNELS)

    # Head-specific methods
    def __str__(self) -> str:
        return f"ParCan | {self.name} {self.get_values()}"