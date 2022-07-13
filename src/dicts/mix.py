from cihai.core import Cihai

from .zdic import ZDict

CIHAI = Cihai()
if not CIHAI.unihan.is_bootstrapped:  # download and install Unihan to db
    CIHAI.unihan.bootstrap({}) # TODO: Unihan options

class MixDict(ZDict):
    def __init__(self, hans) -> None:
        super().__init__(hans)
        self.hans = hans
        self.cihai = CIHAI

    def stroke_num(self) -> int:
        query = self.cihai.unihan.lookup_char(self.hans)
        return query.first().kTotalStrokes
