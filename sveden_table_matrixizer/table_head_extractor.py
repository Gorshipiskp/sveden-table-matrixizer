from typing import Generator

from bs4 import Tag, ResultSet

from .errors import NoTableHeaderError
from .types import ExtractorOptions
from .utils import handle_maybe_async


async def extract_table_head(table: Tag, *, options: ExtractorOptions) -> Tag:
    heads: ResultSet[Tag] = table.find_all("thead")

    if len(heads) == 0:
        raise NoTableHeaderError
    if len(heads) > 1:
        return await handle_maybe_async(options.on_multiply_table_headers, heads)

    return heads[0]


def head_tr_generator(tr_tag: Tag) -> Generator[tuple[Tag, int, int], None, None]:
    for th_tag in tr_tag.find_all("th"):
        th_colspan: int = int(th_tag.get("colspan") or 1)
        th_rowspan: int = int(th_tag.get("rowspan") or 1)

        yield th_tag, th_colspan, th_rowspan


def head_table_generator(table_head: Tag) -> Generator[Generator[tuple[Tag, int, int], None, None], None, None]:
    for tr_tag in table_head.find_all("tr"):
        yield head_tr_generator(tr_tag)


async def extract_table_head_columns(table_head: Tag) -> list[list[Tag]]:
    columns_matrix: list[list[Tag]] = []

    for tr_ind, tr_info in enumerate(head_table_generator(table_head)):
        for th_ind, (th_tag, th_colspan, th_rowspan) in enumerate(tr_info):
            for row_span in range(th_rowspan):
                row_ind: int = tr_ind + row_span

                try:
                    columns_matrix[row_ind]
                except IndexError:
                    columns_matrix.append([])

                for column_span in range(th_colspan):
                    columns_matrix[row_ind].append(th_tag)

    return columns_matrix
