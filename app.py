
from flask import Flask, request, render_template
import asyncio
from pyartnet import ArtNetNode
from fixture import Fixture, PARCAN_CHANNELS

app = Flask(__name__)

# Define Fixtures
fixtures = [
    Fixture(start_channel=16, name='ParCan Left', channel_names=PARCAN_CHANNELS),
    Fixture(start_channel=22, name='ParCan Right', channel_names=PARCAN_CHANNELS),
]

# Define Art-Net node IP
ARTNET_NODE_IP = '192.168.1.221'
FADE_TIME = 100

def get_fixture(name:str) -> Fixture:
    global fixtures
    return next(f for f in fixtures if f.name == name)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/send_artnet', methods=['POST'])
def send_artnet():

    # find the fixture that matches the fixture_name in the request
    fixture = get_fixture(request.form.get('fixture_name'))

    old_values = fixture.get_values()

    if fixture is None:
        return {"error": f"Fixture [{request.form.get('fixture_name')}] not found"}
    
    # get the channel values from the request and set the fixture values
    for channel_name, value in request.form.items():
        if channel_name in fixture.get_channel_names():
            fixture.set_channel_value(channel_name, value)
    
    new_values = fixture.get_values()

    asyncio.run(dispatch_artnet_packet(old_values, new_values))

    # return a json representation of the fixture values
    return fixture.get_values()

async def dispatch_artnet_packet(old_values, new_values):
    start_channel = 16
    # Create an ArtNet node
    node = ArtNetNode(ARTNET_NODE_IP, 6454)
    universe = node.add_universe(0)
    channel = universe.add_channel(start=start_channel, width=len(new_values))
    universe._resize_universe(512)

    # dispatch Artnet packet
    channel.set_values(old_values)
    channel.add_fade(new_values, 10)
    node.start_refresh()
    await channel
    node.stop_refresh()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)