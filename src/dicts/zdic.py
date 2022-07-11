from httpx import get
from parsel import Selector
from utils import retry

from .base import HansDict



class ZDict(HansDict):
    @retry
    def __init__(self, hans,) -> None:
        self.hans = hans
        self.selector = Selector(
            get("https://www.zdic.net/hans/" + hans).text)

    def form_word(self) -> list[str]:
        word_group = self.selector.xpath(
            "//div[@class='cit type-xxjs']//a/text()").getall()
        if not word_group:
            raise ValueError(f"`{self.hans}` 无法组词")
        return word_group

    def stroke_num(self) -> int:
        return int(
            self.selector.xpath(
                "//td[@class='z_bs2']/p[3]/text()").get())