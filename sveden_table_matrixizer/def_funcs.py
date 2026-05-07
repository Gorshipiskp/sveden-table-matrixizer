from dataclasses import dataclass
from typing import Never

from bs4 import Tag, ResultSet

from .errors import MultiplyTableHeaderError, MultiplyTableBodyError


@dataclass(frozen=True, kw_only=True)
class MatrixizedTable:
    head: list[list[Tag]]
    body: list[list[Tag]]


def on_table_no_header_def(_table: Tag, _matrixized_tables: list[MatrixizedTable]) -> None:
    pass


def on_table_no_body_def(_table: Tag, _matrixized_tables: list[MatrixizedTable]) -> None:
    pass


def on_multiply_table_headers_def(_heads: ResultSet[Tag]) -> Never:
    raise MultiplyTableHeaderError


def on_multiply_table_bodies_def(_bodies: ResultSet[Tag]) -> Never:
    raise MultiplyTableBodyError
