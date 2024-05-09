
from flask import Flask, render_template
import yaml
import os
import asyncio
from libs import ArtNetNodeInstance, Channel, create_fixture
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# Define Fixtures
with open('fixtures.yaml', 'r') as file:
    fixtures_data = yaml.safe_load(file)
fixtures = [create_fixture(data) for data in fixtures_data]

# Define Art-Net defaults
ARTNET_NODE_IP = os.getenv('ARTNET_NODE_IP', '192.168.1.221')
FADE_TIME = int(os.getenv('ARTNET_DEFAULT_FADETIME', '1'))

## setup artnet fixtures on startup
# proxy store the artnet channels
artnet_channels = []

# load the fixtures into the artnet node
async def setup_artnet_fixtures(fixtures):
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

# run the fixture setup
with app.app_context():
    print("Setting up ArtNet fixtures")
    asyncio.run(setup_artnet_fixtures(fixtures))

## Flask routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', fixtures=fixtures)

## SocketIO events
@socketio.on('disconnect')
def handle_disconnect():
    print('.. Artnet refresh stopped')
    ArtNetNodeInstance().stop_refresh()

def get_channel_by_id(channel_id)->Channel:
    return next(c for c in artnet_channels if c['name'] == channel_id)['instance']

@socketio.on('slider_change')
def handle_slider_change(data):

    # Get the channel id and value
    channel_id = data['channel_id']
    channel_value = data['value']

    # Get the channel instance
    channel = get_channel_by_id(channel_id)
    channel.next_value = channel_value

    # Dispatch the ArtNet packet
    asyncio.run(dispatch_artnet_packet(channel))


async def dispatch_artnet_packet(channel:Channel):

    # Get the ArtNet node and channel
    node = ArtNetNodeInstance()

    # Set next values and fade
    if channel.next_fade_duration is not None:
        channel.set_fade(channel.next_value, channel.next_fade_duration)
    else:
        channel.set_value(channel.next_value)

    # send and leave the node running
    node.start_refresh()
    await asyncio.sleep(0.01)


## Main loop
if __name__ == '__main__':
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    socketio.run(app, host="0.0.0.0", debug=DEBUG, port=5000, allow_unsafe_werkzeug=True)