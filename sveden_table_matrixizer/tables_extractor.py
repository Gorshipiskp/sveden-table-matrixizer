import asyncio
from dataclasses import dataclass

from bs4 import BeautifulSoup, Tag, ResultSet

from .errors import NoTableHeaderError, NoColumnsInTableHeaderError
from .table_body_extractor import extract_table_body_columns, extract_table_body
from .table_head_extractor import extract_table_head, extract_table_head_columns
from .utils import get_page_bs4


@dataclass(kw_only=True)
class MatrixizedTable:
    head: list[list[Tag]]
    body: list[list[Tag]]
    num_columns: int


async def matrixize_table(table: Tag) -> MatrixizedTable:
    head: Tag = await extract_table_head(table)
    head_columns: list[list[Tag]] = await extract_table_head_columns(head)

    num_columns: int = len(head_columns)

    if num_columns == 0:
        # todo: Сделать супрессор
        raise NoColumnsInTableHeaderError

    body: Tag = await extract_table_body(table)
    body_columns: list[list[Tag]] = await extract_table_body_columns(body)

    return MatrixizedTable(
        head=head_columns,
        body=body_columns,
        num_columns=num_columns,
    )


async def extract_tables(page_bs4: BeautifulSoup) -> ResultSet[Tag]:
    tables = page_bs4.find_all("table")

    return tables


async def matrixize_tables_from_page(url: str) -> list[MatrixizedTable]:
    page_bs4: BeautifulSoup = await get_page_bs4(url)
    tables: ResultSet[Tag] = await extract_tables(page_bs4)

    for table in tables:
        try:
            await matrixize_table(table)
        except NoTableHeaderError:
            print(f"SKIPPED: {NoTableHeaderError.__name__}")


async def main():
    pass


if __name__ == "__main__":
    asyncio.run(main())
