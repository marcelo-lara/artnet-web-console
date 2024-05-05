import sounddevice as sd
import numpy as np

devices = sd.query_devices()
for i, device in enumerate(devices):
    print(f"Device #{i}: {device['name']}")
    
def callback(indata, frames, time, status):
    # This is called (from a separate thread) for each audio block.
    # You can process the audio data here (indata).
    volume_norm = np.linalg.norm(indata) * 10
    print('Volume:', volume_norm)  # For example, print the volume.

with sd.InputStream(callback=callback):
    sd.sleep(10000)  # Record for 10 seconds.