import pathlib
from time import time

from pdfextract import extract

SAMPLE = pathlib.Path(__file__).parent.resolve() / 'sample.pdf'

def test_load():
    path = str(SAMPLE)
    pages_out, chars_out, objs_out, fonts_out = extract(path)

    assert len(chars_out.arrays['char']) == 2913
    assert len(objs_out.arrays['txt_obj_id']) == 36
    assert len(fonts_out.arrays['font_obj_id']) == 3
    assert len(pages_out.arrays['page']) == 1
