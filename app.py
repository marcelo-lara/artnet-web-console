
from flask import Flask, request, render_template, jsonify
import os
import asyncio
from libs.artNetNodeInstance import ArtNetNodeInstance
from libs.fixture import Fixture, Channel
from libs.parCan import ParCan
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Define Fixtures
fixtures = [
    ParCan(start_channel=16, name='ParCan Left'),
    ParCan(start_channel=22, name='ParCan Right'),
]

# Define Art-Net node IP
ARTNET_NODE_IP = os.getenv('ARTNET_NODE_IP', '192.168.1.221')
FADE_TIME = 2

# store the artnet channels
artnet_channels = []
def get_channel_by_id(channel_id)->Channel:
    return next(c for c in artnet_channels if c['name'] == channel_id)['instance']

# setup artnet fixtures on startup
async def setup_artnet_fixtures(fixtures):
    node = ArtNetNodeInstance(ARTNET_NODE_IP, 6454)
    universe = node.add_universe(0)
    for fixture in fixtures:
        for channel in fixture.channels:
            _channel = {
                'name': channel.id,
                'instance': channel,
                'artnet_channel': universe.add_channel(start=channel.number, width=channel.channel_width, channel_name=channel.id)
            }
            artnet_channels.append(_channel)
            
    universe._resize_universe(512)
with app.app_context():
    print("Setting up ArtNet fixtures")
    asyncio.run(setup_artnet_fixtures(fixtures))

def get_fixture(name:str) -> Fixture:
    global fixtures
    return next(f for f in fixtures if f.name == name)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', fixtures=fixtures)

@socketio.on('disconnect')
def handle_disconnect():
    print('.. Artnet refresh stopped')
    ArtNetNodeInstance().stop_refresh()
    
@socketio.on('slider_change')
def handle_slider_change(data):
    # Get the channel id and value
    channel_id = data['channel_id']
    channel_value = data['value']
    
    # Get the channel instance
    channel = get_channel_by_id(channel_id)
    channel.next_value = channel_value
    asyncio.run(dispatch_artnet_packet(channel))
    
async def dispatch_artnet_packet(channel:Channel):

    # Get the ArtNet node and channel
    node = ArtNetNodeInstance()
    node_channel = node.get_universe(0).get_channel(channel.id)
    
    # Set next values and fade
    if channel.next_fade_duration is not None:
        node_channel.set_values([channel.get_value_as_bytes()])
        node_channel.add_fade(channel.next_value, channel.next_fade_duration)
    else:
        node_channel.set_values(channel.get_value_as_bytes())
    channel.complete_send()
    
    # send and leave the node running
    node.start_refresh()
    await asyncio.sleep(0.01)

if __name__ == '__main__':
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    socketio.run(app, host="0.0.0.0", debug=DEBUG, port=5000, allow_unsafe_werkzeug=True)