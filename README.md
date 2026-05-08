# sveden-table-matrixizer

**Extract and matrixize HTML tables from Russian educational organization pages (`/sveden`) with full colspan/rowspan support.**

`sveden-table-matrixizer` is an asynchronous Python library that parses tables found on `/sveden` (сведения об образовательной организации) pages, expands `colspan` and `rowspan` attributes into clean two-dimensional matrices, and returns structured `head` and `body` cell grids. It gives you full control over edge cases via configurable callbacks.

## Features

- **Async page fetching** using `aiohttp`.
- **Full colspan/rowspan expansion** – cells spanning multiple rows and/or columns are duplicated into the matrix.
- **Separate head and body matrix extraction** – each table yields a `head` matrix (from `<thead>`) and a `body` matrix (from `<tbody>`).
- **Customizable error handling** – replace default reactions to missing headers, missing bodies, or multiple `<thead>`/`<tbody>` elements.
- **Lightweight** – only depends on `aiohttp` and `beautifulsoup4`.
- **Works with any HTML** – designed for `/sveden`, but usable on any page containing `<table>` elements.

## Installation

```bash
pip install sveden-table-matrixizer
```

## Quick Start

```python
import asyncio
from sveden_table_matrixizer import matrixize_tables_from_page

async def main():
    url = "https://example.edu/sveden/"
    tables = await matrixize_tables_from_page(url)

    for i, table in enumerate(tables):
        print(f"Table {i+1}:")
        print("  Head rows:", len(table.head))
        print("  Body rows:", len(table.body))
        # Access cells as list[list[bs4.Tag]]

asyncio.run(main())
```

Each `MatrixizedTable` contains:

- `head: list[list[Tag]]` – rows of header cells _(each row is a list of `bs4.Tag`)_.
- `body: list[list[Tag]]` – rows of body cells.

## Handling Edge Cases

By default, the extractor raises exceptions when a table lacks a header or body, or contains more than one `<thead>` / `<tbody>`. You can override this behavior with `ExtractorOptions`.

```python
from sveden_table_matrixizer import matrixize_tables_from_page, ExtractorOptions
from sveden_table_matrixizer.def_funcs import MatrixizedTable

def handle_missing_header(table_tag, collected_tables):
    print(f"Skipping table without <thead>: {table_tag.get('id', 'no id')}")

opts = ExtractorOptions(
    on_table_no_header=handle_missing_header,
    # other callbacks can be set similarly
)

tables = await matrixize_tables_from_page(url, options=opts)
```

You can also supply async callbacks – the library automatically detects and awaits them.

## API Reference

### `matrixize_tables_from_page(url, *, options=None)`

- **Parameters:**
  - `url` (`str`) – URL of the page to scrape.
  - `options` (`ExtractorOptions`, optional) – configuration callbacks.
- **Returns:** `list[MatrixizedTable]` – extracted and matrixized tables.

### `ExtractorOptions`

A frozen dataclass with the following fields (all optional):

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `on_table_no_header` | `Callable[[Tag, list[MatrixizedTable]], Any]` | no‑op | Called when a table has no `<thead>`. |
| `on_table_no_body` | `Callable[[Tag, list[MatrixizedTable]], Any]` | no‑op | Called when a table has no `<tbody>`. |
| `on_multiply_table_headers` | `Callable[[ResultSet[Tag]], Tag \| Never]` | raises `MultiplyTableHeaderError` | Called when more than one `<thead>` is found; must return a single `<thead>` element. |
| `on_multiply_table_bodies` | `Callable[[ResultSet[Tag]], Tag \| Never]` | raises `MultiplyTableBodyError` | Called when more than one `<tbody>` is found; must return a single `<tbody>` element. |

### `MatrixizedTable`

```python
@dataclass(frozen=True, kw_only=True)
class MatrixizedTable:
    head: list[list[Tag]]   # matrix of <th> tags
    body: list[list[Tag]]   # matrix of <td> tags
```

### Exceptions

- `NoTableHeaderError` – raised when `options.on_table_no_header` is not overridden.
- `NoTableBodyError` – raised when `options.on_table_no_body` is not overridden.
- `MultiplyTableHeaderError` – default reaction to multiple `<thead>` elements.
- `MultiplyTableBodyError` – default reaction to multiple `<tbody>` elements.

All exceptions are exported from `sveden_table_matrixizer.errors`.

## How It Works

1. The page is fetched with `aiohttp` and parsed by BeautifulSoup.
2. All `<table>` tags are collected.
3. For each table:
   - The `<thead>` is located; if missing or duplicate, the appropriate callback is invoked.
   - The `<tbody>` is located similarly.
   - Header rows are expanded: each `<th>` with `colspan`/`rowspan` is replicated into the correct cells of a 2D list.
   - The same expansion is applied to body rows using `<td>` elements.
4. A `MatrixizedTable(head=..., body=...)` is created and added to the result list.

## Dependencies

- Python ≥ 3.11
- [aiohttp](https://pypi.org/project/aiohttp/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

## License

This project is licensed under the MIT License – see the source repository for details.