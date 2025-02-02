import os
import pathlib

SAMPLE = pathlib.Path(__file__).parent.resolve() / 'sample.pdf'

def test_load():
    import os
    print()
    print(os.getcwd())

    from pathlib import Path
    from time import time

    from pdfextract import extract
    from pdfextract.table import CharTable

    path = (str(SAMPLE)).encode('utf-8')

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

