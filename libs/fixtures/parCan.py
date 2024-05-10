from libs.fixtures.fixture import Fixture
PARCAN_CHANNELS = ['fader', 'red', 'green', 'blue', 'strobe', 'colors']


class ParCan(Fixture):
    def __init__(self, start_channel, name, **kwargs):
        super().__init__(start_channel, name, channel_names=PARCAN_CHANNELS)

    # Add any ParCan-specific methods here
    def __str__(self) -> str:
        return f"ParCan | {self.name} {self.get_values()}"