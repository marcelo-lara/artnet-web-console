from typing import Collection, Union


class Channel:
    """
    Represents a channel of a fixture.
    """
    def __init__(self, name: str, number: int, channel_width: int = 1):
        """
        Initializes a Channel object.

        Parameters:
        - name (str): The name of the channel.
        - number (int): The channel number in the universe.
        - channel_width (int): The width of the channel in bytes. Default value is 1 (8bits).

        Returns:
        - None
        """
        self.name = name  # Set channel name
        self.number = number  # Set channel number in universe
        self.channel_width = channel_width  # Set channel width
        self.value = 0  # Last value sent to the channel
        self.id = f"ch{self.number}_{self.name}"
        
        self.next_value = None # Next value to be sent to the channel
        self.next_fade_duration = None # Duration of the fade in milliseconds
        
        self._instance = None  # ArtNetNode instance of the channel

    def set_value(self, value):
        """
        Sets the value of the channel.

        Parameters:
        - value (int): The value to set.

        Returns:
        - new channel value
        """
        if self._instance is not None:
            self._instance.set_values(self.get_value_as_bytes(value))
            
        self.complete_send()
        return self.value
    
    def set_fade(self, target_value, time):
        """
        Sets the value of the channel with a fade duration.

        Parameters:
        - value (int): The value to set.
        - time (int): The duration of the fade in milliseconds.

        Returns:
        - new channel value
        """
        if self._instance is not None:
            self._instance.add_fade(self.get_value_as_bytes(target_value), time)
            
        self.complete_send()
        return self.value
    
    def get_value_as_bytes(self, value=None)->Collection[Union[int, float]]:
        """
        Returns the current value of the channel.

        Parameters:
        - None

        Returns:
        - int: The current value of the channel.
        """
        if value is not None:
            return [int(value)]
        else:
            return [int(self.value)]
    
    def complete_send(self):
        # Store last value sent
        self.value = self.next_value
        
        # Reset next value and fade duration
        self.next_value = None
        self.next_fade_duration = None
        

    def __str__(self) -> str:
        return f"Channel|{self.name}|dmx{self.number}|val{self.value}"