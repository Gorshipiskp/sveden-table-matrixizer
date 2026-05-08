from dataclasses import dataclass
from typing import Callable, Any, Never, Sequence

from bs4 import Tag

from .def_funcs import MatrixizedTable, on_table_no_header_def, on_table_no_body_def, on_multiply_table_headers_def, \
    on_multiply_table_bodies_def


@dataclass(frozen=True, kw_only=True)
class ExtractorOptions:
    on_table_no_header: Callable[[Tag, Sequence[MatrixizedTable]], Any] = on_table_no_header_def
    on_table_no_body: Callable[[Tag, Sequence[MatrixizedTable]], Any] = on_table_no_body_def
    on_multiply_table_headers: Callable[[Sequence[Tag]], Tag | Never] = on_multiply_table_headers_def
    on_multiply_table_bodies: Callable[[Sequence[Tag]], Tag | Never] = on_multiply_table_bodies_def
