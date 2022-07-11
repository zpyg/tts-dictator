from httpx import get
from parsel import Selector
from tenacity import retry, stop_after_attempt, wait_fixed

from .base import HansDict


# TODO: ABC
class ZDict(HansDict):

    @retry(stop=stop_after_attempt(2), wait=wait_fixed(2))
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

    # def _check_empty(self, obj):
    #     "return obj if it's not empty else raise an error"
    #     if not obj:
    #         raise ValueError
    #     return obj
