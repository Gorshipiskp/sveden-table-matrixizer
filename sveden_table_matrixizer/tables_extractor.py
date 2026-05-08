from bs4 import BeautifulSoup, Tag, ResultSet

from .def_funcs import MatrixizedTable
from .errors import NoTableHeaderError, NoTableBodyError
from .table_body_extractor import extract_table_body_columns, extract_table_body
from .table_head_extractor import extract_table_head, extract_table_head_columns
from .types import ExtractorOptions
from .utils import get_page_bs4, handle_maybe_async


async def matrixize_table(table: Tag, options: ExtractorOptions) -> MatrixizedTable:
    head: Tag = await extract_table_head(table, options=options)
    head_columns: list[list[Tag]] = await extract_table_head_columns(head)

    body: Tag = await extract_table_body(table, options=options)
    body_columns: list[list[Tag]] = await extract_table_body_columns(body)

    return MatrixizedTable(
        head=head_columns,
        body=body_columns
    )


async def extract_tables(page_bs4: BeautifulSoup) -> ResultSet[Tag]:
    tables: ResultSet[Tag] = page_bs4.find_all("table", recursive=False)

    return tables


async def matrixize_tables_from_page(url: str, *, options: ExtractorOptions | None = None) -> list[MatrixizedTable]:
    if options is None:
        options = ExtractorOptions()

    page_bs4: BeautifulSoup = await get_page_bs4(url)
    tables: ResultSet[Tag] = await extract_tables(page_bs4)

    matrixized_tables: list[MatrixizedTable] = []
    for table in tables:
        try:
            matrixized_table: MatrixizedTable = await matrixize_table(table, options=options)

            matrixized_tables.append(matrixized_table)
        except NoTableHeaderError:
            await handle_maybe_async(options.on_table_no_header, table, matrixized_tables)
        except NoTableBodyError:
            await handle_maybe_async(options.on_table_no_body, table, matrixized_tables)

    return matrixized_tables
