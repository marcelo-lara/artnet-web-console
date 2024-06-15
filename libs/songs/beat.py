class Beat:
    """
    Represents a Beat of a song.
    """
    def __init__(self, beat_data: dict):
        self.curr_beat_time = beat_data.get('curr_beat_time', 0)
        self.curr_beat = beat_data.get('curr_beat', 0)
        self.bar_num = beat_data.get('bar_num', 0)
        self.beat_num = beat_data.get('beat_num', 0)
        self.prev_chord = beat_data.get('prev_chord', "")
        self.chord_complex_jazz = beat_data.get('chord_complex_jazz', "")
        self.chord_simple_jazz = beat_data.get('chord_simple_jazz', "")
        self.chord_complex_pop = beat_data.get('chord_complex_pop', "")
        self.chord_simple_pop = beat_data.get('chord_simple_pop', "")
        self.bass = beat_data.get('bass', None)

    def __str__(self):
        return f"{self.chord_complex_pop}"