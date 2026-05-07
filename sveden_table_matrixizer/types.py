from dataclasses import dataclass
from typing import Callable, Any, Never

from bs4 import Tag

from sveden_table_matrixizer.def_funcs import MatrixizedTable, on_table_no_header_def, on_table_no_body_def, \
    on_multiply_table_headers_def, on_multiply_table_bodies_def


@dataclass(frozen=True, kw_only=True)
class ExtractorOptions:
    on_table_no_header: Callable[[Tag, list[MatrixizedTable]], Any] = on_table_no_header_def
    on_table_no_body: Callable[[Tag, list[MatrixizedTable]], Any] = on_table_no_body_def
    on_multiply_table_headers: Callable[[Tag, list[list[Tag]]], Tag | Never] = on_multiply_table_headers_def
    on_multiply_table_bodies: Callable[[Tag, list[list[Tag]]], Tag | Never] = on_multiply_table_bodies_def
