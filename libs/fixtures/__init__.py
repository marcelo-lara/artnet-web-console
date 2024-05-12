from libs.fixtures.fixture import Channel
from libs.fixtures.parCan import ParCan
from libs.fixtures.head import Head
from libs.fixtures.channel import Channel
from libs.artNetNodeInstance import ArtNetNodeInstance
import os

# Define Art-Net defaults
ARTNET_NODE_IP = os.getenv('ARTNET_NODE_IP', '192.168.1.221')
FADE_TIME = int(os.getenv('ARTNET_DEFAULT_FADETIME', '1'))

fixture_types = {
    'Head': Head,
    'ParCan': ParCan
}

def create_fixture(data):
    fixture_type = data.get('type')
    if fixture_type in fixture_types:
        return fixture_types[fixture_type](**data)
    else:
        raise ValueError(f"Unknown fixture type: {fixture_type}")
    
async def setup_artnet_fixtures(fixtures, artnet_channels=[]):
    print("Setting up ArtNet fixtures")
    
    node = ArtNetNodeInstance(ARTNET_NODE_IP, 6454)
    universe = node.add_universe(0)
    for fixture in fixtures:
        for channel in fixture.channels:
            channel._instance = universe.add_channel(start=channel.number, width=channel.channel_width, channel_name=channel.id)
            _channel = {
                'name': channel.id,
                'instance': channel
            }
            artnet_channels.append(_channel)
    universe._resize_universe(512)