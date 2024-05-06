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

    def set_value(self, value):
        """
        Sets the value of the channel.

        Parameters:
        - value (int): The value to set.

        Returns:
        - new channel value
        """
        self.value = value
        return self.value
    
    def complete_send(self):
        # Store last value sent
        self.value = self.next_value
        
        # Reset next value and fade duration
        self.next_value = None
        self.next_fade_duration = None
        

    def __str__(self) -> str:
        return f"Channel|{self.name}: {self.number})"