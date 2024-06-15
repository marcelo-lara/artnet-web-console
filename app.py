
from flask import Flask, render_template
import yaml
import os
import asyncio
from libs import ArtNetNodeInstance, Channel, Chaser, Song, Beat
from libs.fixtures import setup_artnet_fixtures, create_fixture
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)


## Define Fixtures
with open('fixtures.yaml', 'r') as file:
    fixtures_data = yaml.safe_load(file)
fixtures = [create_fixture(data) for data in fixtures_data]

## setup artnet fixtures on startup
artnet_channels = []
with app.app_context():
    asyncio.run(setup_artnet_fixtures(fixtures, artnet_channels))

## Read the song data from songbooks folder into a Song object
song = Song()
song.load_from_file('static/songbook/obsession.json')


## Flask routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', fixtures=fixtures, song=song)

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

## Chaser Handler ##################################################################################
chaser = None
async def _chaser_movenext():
    global chaser
    while chaser.is_playing:
        await chaser.movenext()
        await asyncio.sleep(60 / chaser.bpm)
              
@socketio.on('connect')
def handle_connect():
    global chaser
    chaser = Chaser(socketio, bpm=120, s_beat=artnet_channels)

@socketio.on('chaser_start')
def handle_start_chaser(data):
    global chaser
    if chaser is not None:
        asyncio.run(chaser.start())
        asyncio.run(_chaser_movenext())

@socketio.on('chaser_stop')
def handle_stop_chaser(data=None):
    global chaser
    if chaser is not None:
        asyncio.run(chaser.stop())

@socketio.on('chaser_reset')
def handle_reset_chaser(data=None):
    global chaser
    if chaser is not None:
        asyncio.run(chaser.reset())

@socketio.on('chaser_set_bpm')
def handle_set_bpm(data=None):
    newBpm = int(data['bpm'])
    global chaser
    if chaser is not None:
        asyncio.run(chaser.setBpm(newBpm))


        
## Main loop
if __name__ == '__main__':
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    socketio.run(app, host="0.0.0.0", debug=DEBUG, port=5000, allow_unsafe_werkzeug=True)