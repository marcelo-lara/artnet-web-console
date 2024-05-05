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