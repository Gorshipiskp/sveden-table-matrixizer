import inspect
from typing import Coroutine, TypeVar, Awaitable, Callable

from aiohttp import ClientSession
from bs4 import BeautifulSoup


async def get_page_bs4(url: str) -> BeautifulSoup:
    async with ClientSession() as session:
        async with session.get(url) as response:
            return BeautifulSoup(await response.text(), "html.parser")


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
