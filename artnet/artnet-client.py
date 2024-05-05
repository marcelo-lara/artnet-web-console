import time
import sys
import python_artnet as Artnet
from os import system

debug = False

# What DMX channels we want to listen to
dmxChannels = [16,17,18,19]

### ArtNet Config ###
artnetBindIp = "0.0.0.0"
artnetUniverse = 0

### Art-Net Setup ###
# Sets debug in Art-Net module.
# Creates Artnet socket on the selected IP and Port
artNet = Artnet.Artnet(artnetBindIp, DEBUG=debug)
system('clear')

while True:
    try:
        print(f"{time.strftime("%H:%M:%S", time.localtime())}", end=" ")

        # Gets whatever the last Art-Net packet we received is
        artNetPacket = artNet.readPacket()

        # Make sure we actually *have* a packet
        if artNetPacket is not None and artNetPacket.data is not None:
            # Checks to see if the current packet is for the specified DMX Universe
            if artNetPacket.universe == artnetUniverse:
                # Stores the packet data array
                dmxPacket = artNetPacket.data
                
                # Then print out the data from each channel
                print("Received data: ", end="")
                for i in dmxChannels:
                    # Lists in python start at 0, so to access a specific DMX channel you have to subtract one
                    print(dmxPacket[i-1], end=" ")
                
                # Print a newline so things look nice :)
                print("", end="\r")
                
        time.sleep(0.1)
        
    except KeyboardInterrupt:
        break

# Close the various connections cleanly so nothing explodes :)
artNet.close()
sys.exit()