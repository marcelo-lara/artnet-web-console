import json
from libs.songs.beat import Beat

class Song:
    """
    Represents a Song with a sequence of beats.
    """

    def __init__(self):
        self.beats = []
        self.curr_beat = 0
        self.bpm = 120
    
    def load_from_file(self, filename:str):
        """
        Load a song from a file.
        """
        with open(filename, 'r') as file:
            data = json.load(file)
            self.beats = list(map(lambda x: Beat(x), data))