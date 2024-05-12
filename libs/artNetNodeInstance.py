from pyartnet import ArtNetNode


class ArtNetNodeInstance:
    _instance = None

    def __new__(cls, *args, **kwargs)->ArtNetNode:
        if not cls._instance:
            cls._instance = ArtNetNode(*args, **kwargs)
        return cls._instance