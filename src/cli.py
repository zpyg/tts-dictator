#!/usr/bin/env python
import argparse
from pathlib import Path
from time import sleep

from dicts.zdic import ZDict as HansDict
from speakers.google import GoogleTTS as Speaker


def eval_wait_time(text, weight_person: int | float = 0):
    """预估等待时长
    Args:
        weight_person (int | float, optional): 自己书写速度的权重，可为正数或负数. Defaults to 0.
    """
    # TODO: 可以对指定字数、笔画数设定时间
    # TODO: 想一个更好的算法，或基于统计
    # 根据长度估计书写时长
    weight_len = len(text) * 1.2
    # 根据笔画数估计书写时长
    weight_stroke = sum([HansDict(char).stroke_num() * 0.1 for char in text])
    # 综合长度、笔画，再加上个人调整
    return weight_len + weight_stroke + weight_person

def cli_argparser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    # TODO: 命令行读取更多配置 {image-orc, reapet-time, personal-weight, config-file, ...} 或者直接整 GUI
    parser.add_argument("file", help="input file")
    return parser.parse_known_args()[0]

if __name__ == '__main__':
    # TODO: 规范化配置
    vars = cli_argparser()
    REPEAT_TIME = 2
    PERSONAL_WEIGHT = -1

    # load words (except empty item)
    words = Path(vars.file).read_text().split('\n')[:-1]
    for n in range(len(words)):
        word = words[n]
        wait_time = eval_wait_time(word, PERSONAL_WEIGHT) # 必须放在这，放下面自动组词后它会计算 “xx 的 x”的书写时间，不改了，就这样吧
        # 给单字组词
        if len(word) == 1:
            try:
                word = f"{HansDict(word).form_word()[0]} 的 {word}"
            except ValueError: # 组词失败则使用原词
                pass
        # 初始化 speaker
        with Speaker(f"第{n+1}个: {word}。", lang="zh", tld="cn",slow= True) as speaker:
            # 重复
            for _ in range(REPEAT_TIME):
                speaker.say()
                if REPEAT_TIME > 1:
                    sleep(wait_time)
