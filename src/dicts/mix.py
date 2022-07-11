from cihai.core import Cihai

from .zdic import ZDict

class MixDict(ZDict):
    def __init__(self, hans, unihan_options={}) -> None:
        # TODO: 重构字典模式 避免反复初始化
        super().__init__(hans)
        self.hans = hans
        self.cihai = Cihai()
        if not self.cihai.unihan.is_bootstrapped:  # download and install Unihan to db
            self.cihai.unihan.bootstrap(unihan_options)

    def stroke_num(self) -> int:
        query = self.cihai.unihan.lookup_char(self.hans)
        return query.first().kTotalStrokes
