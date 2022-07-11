from abc import ABCMeta, abstractmethod

class Speaker(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, text: str, **tts_args):
        ...

    @abstractmethod
    def say(self):
        ...

    @abstractmethod
    def __enter__(self):
        ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        ...
