from .base import Speaker

class PaddleSpeech(Speaker):
    def __init__(self, text: str, **tts_args):
        super().__init__(text, **tts_args)

    def say(self):
        return super().say()

    def __enter__(self):
        return super().__enter__()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        return super().__exit__(exc_type, exc_val, exc_tb)
