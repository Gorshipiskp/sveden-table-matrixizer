from typing import Literal

from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag

STR_CLEAN_SYMBOLS = Literal["\n", "\t", "\r", "  "]


async def get_page_bs4(url: str) -> BeautifulSoup:
    async with ClientSession() as session:
        async with session.get(url) as response:
            return BeautifulSoup(await response.text(), "html.parser")


def clean_str(s: str, *to_save: STR_CLEAN_SYMBOLS) -> str:
    if "\n" not in to_save:
        s = s.replace("\n", " ")
    if "\t" not in to_save:
        s = s.replace("\t", " ")
    if "\r" not in to_save:
        s = s.replace("\r", " ")

    if "  ":
        while "  " in s:
            s = s.replace("  ", " ")

    return s.strip()


def get_text_tag_content(tag: Tag, *to_save: STR_CLEAN_SYMBOLS) -> str:
    # todo: Сделать возможность выбора способа извлечения (можно вынести в выбор в классе)
    content = tag.get("data-content", tag.text)

    return clean_str(content, *to_save)
