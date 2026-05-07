from typing import Generator

from bs4 import Tag, ResultSet

from .errors import NoTableBodyError
from .types import ExtractorOptions
from .utils import handle_maybe_async


async def extract_table_body(table: Tag, *, options: ExtractorOptions) -> Tag:
    bodies: ResultSet[Tag] = table.find_all("tbody")

    if len(bodies) == 0:
        raise NoTableBodyError
    if len(bodies) > 1:
        return await handle_maybe_async(options.on_multiply_table_bodies, bodies)

    return bodies[0]


def body_tr_generator(tr_tag: Tag) -> Generator[tuple[Tag, int, int], None, None]:
    for td_tag in tr_tag.find_all("td"):
        td_colspan: int = int(td_tag.get("colspan") or 1)
        td_rowspan: int = int(td_tag.get("rowspan") or 1)

        yield td_tag, td_colspan, td_rowspan


def body_table_generator(table_body: Tag) -> Generator[Generator[tuple[Tag, int, int], None, None], None, None]:
    for tr_tag in table_body.find_all("tr"):
        yield body_tr_generator(tr_tag)


async def extract_table_body_columns(table_body: Tag) -> list[list[Tag]]:
    columns_matrix: list[list[Tag]] = []

    for tr_ind, tr_info in enumerate(body_table_generator(table_body)):
        for td_ind, (td_tag, td_colspan, td_rowspan) in enumerate(tr_info):
            for row_span in range(td_rowspan):
                row_ind: int = tr_ind + row_span

                try:
                    columns_matrix[row_ind]
                except IndexError:
                    columns_matrix.append([])

                for column_span in range(td_colspan):
                    columns_matrix[row_ind].append(td_tag)

    return columns_matrix
