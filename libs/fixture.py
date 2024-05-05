from typing import Collection, Union

class Channel:
    """
    Represents a channel of a fixture.
    """
    def __init__(self, name: str, number: int, channel_width: int = 8):
        """
        Initializes a Channel object.

        Parameters:
        - name (str): The name of the channel.
        - number (int): The channel number in the universe.
        - channel_width (int): The width of the channel in bits. Default value is 8bits.

        Returns:
        - None
        """
        self.name = name  # Set channel name
        self.number = number  # Set channel number in universe
        self.channel_width = channel_width  # Set channel width
        self.current_value = 0  # Last value sent to the channel

    def set_value(self, value):
        """
        Sets the value of the channel.

        Parameters:
        - value (int): The value to set.

        Returns:
        - new channel value
        """
        self.current_value = value
        return self.current_value

    def __str__(self) -> str:
        return f"Channel|{self.name}: {self.number})"

class Fixture:
    """
    Represents a fixture with multiple channels.
    """

    def __init__(self, start_channel: int, name: str, channel_names: list):
        """
        Initializes a Fixture object.

        Parameters:
        - start_channel (int): The starting channel number.
        - name (str): The name of the fixture.
        - channel_names (list): A list of channel names.

        Returns:
        - None
        """
        self.start_channel = start_channel  # Set starting channel number
        self.channels = [Channel(name, i) for i, name in enumerate(channel_names, start=start_channel)]
        self.name = name  # Set name
        
    def get_values(self)->Collection[Union[int, float]]:
        """
        Returns the current values of all fixture channels.
        Parameters:
        - None

        """
        return [int(channel.current_value) for channel in self.channels]

    def get_name(self):
        """
        Returns the name of the fixture.

        Parameters:
        - None

        Returns:
        - str: The name of the fixture.
        """
        return self.name

    def get_channel_value(self, channel_name):
        """
        Returns the current value of a specific channel.

        Parameters:
        - channel_name (str): The name of the channel.

        Returns:
        - int: The current value of the channel.
        - None: If no channel with the given name is found.
        """
        for channel in self.channels:
            if channel.name == channel_name:
                return channel.get_value()
        return None  # Return None if no channel with the given name is found
    
    def set_channel_value(self, channel_name, value):
        """
        Sets the value of a specific channel.

        Parameters:
        - channel_name (str): The name of the channel.
        - value (int): The value to set.

        Returns:
        - None

        Raises:
        - ValueError: If no channel with the given name is found.
        """
        channel = next((c for c in self.channels if c.name == channel_name), None)
        if channel is not None:
            channel.set_value(value)
        else:
            raise ValueError(f"Channel {channel_name} not found")

    def get_channel_names(self):
        """
        Returns a list of channel names.

        Parameters:
        - None

        Returns:
        - list: A list of channel names.
        """
        return [channel.name for channel in self.channels]
    
    def set_channel_values(self, values: dict):
        """
        Sets the values of multiple channels.

        Parameters:
        - values (dict): A dictionary with channel names as keys and channel values as values.

        Returns:
        - a dictionary of channel number and their new values, ordered by channel number.

        Raises:
        - ValueError: If a channel with a given name is not found.
        """
        for channel_name, value in values.items():
            channel = next((c for c in self.channels if c.name == channel_name), None)
            if channel is not None:
                channel.set_value(value)
            else:
                raise ValueError(f"Channel {channel_name} not found")
        ordered_values = {channel.number: channel.current_value for channel in self.channels}
        return dict(sorted(ordered_values.items(), key=lambda x: x[0]))
    
    def to_dict(self):
        sorted_channels = sorted(self.channels, key=lambda channel: channel.number)
        print({channel.name: channel.current_value for channel in sorted_channels})
        return {
            'type': self.__class__.__name__,
            'name': self.name,
            'start_channel': self.start_channel,
            'channels': {channel.name: channel.current_value for channel in sorted_channels}  
        }    