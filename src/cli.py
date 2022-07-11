import tempfile
from time import sleep
from pathlib import Path
import argparse

from gtts import gTTS, gTTSError
from playsound import playsound
from tenacity import retry, stop_after_attempt, wait_fixed
#from rich.console import Console

from dicts.zdic import ZDict as HansDict


@retry(stop=stop_after_attempt(2), wait=wait_fixed(2))
def dictate(text: str, gap: int, times: int = 1, **tts_args):
    with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as audio:
        gTTS(text, **tts_args).save(audio.name)
        # repeat
        for _ in range(times):
            playsound(audio.name)
            if times > 1:
                sleep(gap)

# TODO: fn
def eval_gap(text):
    w_len = len(text) * 1.5
    w_storke = ...

if __name__ == '__main__':
    # arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="input file")
    # TODO: 命令行参数
    vars, _ = parser.parse_known_args()

    # load words (except empty item)
    words = Path(vars.file).read_text().split('\n')[:-1]
    for n in range(len(words)):
        word = words[n]
        # TODO: 合理 抽象函数
        speaker = lambda gap: dictate(f"第{n+1}个: {word}。", times=2, gap=gap, lang="zh-CN", tld='cn', slow=True)
        # 使用 eval_gap 函数重构
        match len(word):
            case 1:
                # TODO: 可选组词
                try:
                    # TODO: 听不清，换一个词
                    # TODO: 抽象二级speaker
                    dictate(f"第{n+1}个: {HansDict(word).form_word()[0]} 的 {word}。", times=2, gap=1, lang="zh-CN", tld='cn', slow=True)
                except ValueError: # 无法组词
                    speaker(2)
            case 2:
                speaker(3)
            case 4:
                speaker(5)
            case _n:
                speaker(3)
