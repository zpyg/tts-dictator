from abc import ABCMeta, abstractmethod

class Speaker(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, text: str, **tts_args):
        ...

    @abstractmethod
    def say(self):
        ...
