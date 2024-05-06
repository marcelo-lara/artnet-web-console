
from flask import Flask, request, render_template, jsonify
import asyncio
from libs.artNetNodeInstance import ArtNetNodeInstance
from libs.fixture import Fixture
from libs.parCan import ParCan

app = Flask(__name__)

# Define Fixtures
fixtures = [
    ParCan(start_channel=16, name='ParCan Left'),
    ParCan(start_channel=22, name='ParCan Right'),
]

# Define Art-Net node IP
ARTNET_NODE_IP = '192.168.1.221'
FADE_TIME = 2

@app.before_first_request
def setup():
    print("Setting up ArtNet fixtures")
    asyncio.run(setup_artnet_fixtures(fixtures))

async def setup_artnet_fixtures(fixtures):
    node = ArtNetNodeInstance(ARTNET_NODE_IP, 6454)
    universe = node.add_universe(0)
    for fixture in fixtures:
        universe.add_channel(start=fixture.start_channel, width=len(fixture.get_values()), channel_name=fixture.id)
    universe._resize_universe(512)

def get_fixture(name:str) -> Fixture:
    global fixtures
    return next(f for f in fixtures if f.name == name)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', fixtures=fixtures)

@app.route('/fixtures', methods=['GET'])
def get_fixtures():
    global fixtures
    return jsonify([f.to_dict() for f in fixtures])

@app.route('/send_artnet', methods=['POST'])
def send_artnet():
    data = request.get_json()

    # find the fixture that matches the fixture_name in the request
    fixture = get_fixture(data.get('fixture_name'))
    if fixture is None:
        return {"error": f"Fixture [{data.get('fixture_name')}] not found"}
    
    # get the channel values from the request and set the fixture values
    channels = data.get('channels')
    for channel in channels:
        channel_name = channel.get('name')
        channel_value = channel.get('value')

        if channel_name in fixture.get_channel_names():
            fixture.set_channel_value(channel_name, channel_value)

    new_values = fixture.get_values()

    asyncio.run(dispatch_artnet_packet(fixture, new_values))

    # return a json representation of the fixture values
    return fixture.get_values()

async def dispatch_artnet_packet(fixture:Fixture, new_values):
    
    # Create an ArtNet node
    node = ArtNetNodeInstance(ARTNET_NODE_IP, 6454, refresh_every=0.1, max_fps=30)
    channel = node.get_universe(0).get_channel(fixture.id)
    channel.set_values(new_values)
    # channel.add_fade(new_values, 0.1)
    node.start_refresh()
    await asyncio.sleep(0.01)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)