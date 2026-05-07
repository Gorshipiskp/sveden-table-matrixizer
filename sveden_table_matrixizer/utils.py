import inspect
from typing import Literal, Coroutine, TypeVar, Awaitable, Callable

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

    if "  " not in to_save:
        while "  " in s:
            s = s.replace("  ", " ")

    return s.strip()


def get_text_tag_content(tag: Tag, *to_save: STR_CLEAN_SYMBOLS) -> str:
    content = tag.get("data-content", tag.text)

    return clean_str(content, *to_save)


T = TypeVar("T")


async def handle_maybe_async(func: Coroutine[..., ..., T] | Callable[..., T | Awaitable[T]] | T, *args, **kwargs) -> T:
    if inspect.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    if inspect.iscoroutine(func):
        return await func
    if not inspect.isfunction(func):
        return func

    result: T = func(*args, **kwargs)

    if inspect.isawaitable(result):
        return await result

    return result
