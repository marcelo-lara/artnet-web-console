import asyncio
from pyartnet import ArtNetNode

async def main():
    # Run this code in your async function
    node = ArtNetNode(
        '192.168.1.221', 
        6454,
        max_fps=30,
        start_refresh_task=False, 
        sequence_counter=True)


    # Create universe 0
    universe = node.add_universe(0)

    # Add a channel to the universe which consists of 3 values
    # Default size of a value is 8Bit (0..255) so this would fill
    # the DMX values 1..3 of the universe
    channel = universe.add_channel(
        start=16, 
        width=4,
        byte_size=1
    )
    
    universe._resize_universe(512)

    # Fade channel to 255,0,0 in 5s
    # The fade will automatically run in the background

    channel.set_values([0]*4)
    channel.add_fade([255]*4, 1000)

    # this can be used to wait till the fade is complete
    await channel

asyncio.run(main())