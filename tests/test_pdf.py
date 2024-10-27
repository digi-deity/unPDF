from charminator import extract
from pathlib import Path
import pandas as pd
from time import time
import pyarrow as pa
from charminator.table import CharTable

def test_table():
    tbl = CharTable(100)
    print(tbl)

def test_load():
    path = (str(Path('./tests/sample.pdf').resolve())).encode('utf-8')

    start = time()
    pages_out, chars_out, objs_out, fonts_out = extract(path)
    end = time()
    duration = end - start
    print(f'{duration:.3f}s')

    df_chars = chars_out.table.to_pandas()
    df_objs = objs_out.table.to_pandas()
    df_fonts = fonts_out.table.to_pandas()
    df_pages = pages_out.table.to_pandas()

    print(1)

