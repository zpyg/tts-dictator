from abc import ABCMeta, abstractmethod


class HansDict(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, hans: str) -> None:
        ...

    @abstractmethod
    def form_word(self) -> list[str]:
        """给汉字组词
        Retrun: 包含该汉字的词语列表
        """
        ...

    @abstractmethod
    def stroke_num(self) -> int:
        """获取汉字笔画数
        Retrun: 笔画数
        """
        ...
