from tempfile import NamedTemporaryFile

from gtts import gTTS
from playsound import playsound
from utils import retry

from .base import Speaker


class GoogleTTS(Speaker):
    @retry
    def __init__(self, text: str, **tts_args):
        """
        >>> with GoogleTTS('hello') as tts:
        >>>     tts.say()
        """
        self.text = text
        self.tts_args = tts_args
        
        self.audio = NamedTemporaryFile(delete=True, suffix='.mp3')
        gTTS(self.text, **self.tts_args).save(self.audio.name)

    def say(self):
        playsound(self.audio.name)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.audio.close()
