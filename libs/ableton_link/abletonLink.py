from aalink import Link

class AbletonLink: 
    _instance = None

    def __new__(cls, *args, **kwargs)->Link:
        if not cls._instance:
            cls._instance = Link(*args, **kwargs)
        return cls._instance