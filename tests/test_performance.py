from __future__ import annotations

import time
import pytest
import pathlib
from ctypes import byref, c_int, create_string_buffer

from unpdf import extract

PDF_DIR = pathlib.Path(__file__).parent.resolve() / 'pdfs'

def pdfium_extract(pdf, with_info: bool = False):
    import pypdfium2 as pdfium

    pages = []

    pdf = pdfium.PdfDocument(pdf)

    for page_idx in range(len(pdf)):
        page = pdf.get_page(page_idx)
        textpage = page.get_textpage()
        if with_info:
            chars = get_chars_info(textpage)
        else:
            chars = textpage.get_text_bounded()
        pages.append(chars)

    pdf.close()

    return pages


def get_chars_info(textpage):
    import pypdfium2.raw as pdfium_c
    chars = []

    for i in range(textpage.count_chars()):
        text = chr(pdfium_c.FPDFText_GetUnicode(textpage, i))

        rotation = pdfium_c.FPDFText_GetCharAngle(textpage, i)

        char_box = textpage.get_charbox(i)

        font_name_str = ""
        flags = 0
        try:
            buffer_size = 256
            font_name = create_string_buffer(buffer_size)
            font_flags = c_int()

            length = pdfium_c.FPDFText_GetFontInfo(textpage, i, font_name, buffer_size, byref(font_flags))
            if length > buffer_size:
                font_name = create_string_buffer(length)
                pdfium_c.FPDFText_GetFontInfo(textpage, i, font_name, length, byref(font_flags))

            if length > 0:
                font_name_str = font_name.value.decode('utf-8')
                flags = font_flags.value
        except:
            pass

        fontsize = pdfium_c.FPDFText_GetFontSize(textpage, i)
        fontweight = pdfium_c.FPDFText_GetFontWeight(textpage, i)

        char_dict = {
            "bbox": char_box,
            "char": text,
            "rotation": rotation,
            "font": {
                "name": font_name_str,
                "flags": flags,
                "size": fontsize,
                "weight": fontweight,
            },
            "char_idx": i
        }
        chars.append(char_dict)

    return chars

@pytest.mark.skip("This test is for performance benchmarking and may take a long time to run.")
@pytest.mark.parametrize("filename", [
    "the_wonderful_wizard_of_oz.pdf", "nvidia-annual-report-2025.pdf", "jane_eyre.pdf"
])
def test_benchmark(filename):
    print("filename:", filename)
    filepath = PDF_DIR / filename

    durations = {}

    # First test performance of the pdfium_extract function
    start_time = time.time()
    pages = pdfium_extract(filepath, with_info=True)

    end_time = time.time()
    durations['PyPDFium2'] = end_time - start_time

    # Now test performance of the extract function from unpdf
    start_time = time.time()
    pages_out, chars_out, objs_out, fonts_out = extract(str(filepath))
    end_time = time.time()
    durations['unPDF'] = end_time - start_time

    # First test performance of the pdfium_extract function
    start_time = time.time()
    pages = pdfium_extract(filepath, with_info=False)

    end_time = time.time()
    durations['Optimum'] = end_time - start_time

    print("\nFile:", filename, ", Pages:", len(pages))
    print(f"  {'unPDF detailed characters duration':<40}: {durations['unPDF']:.4f} (1.00x) seconds")
    print(f"  {'PyPDFium2 detailed characters duration':<40}: {{:.4f}} ({{:.2f}}x) seconds".format(
        durations['PyPDFium2'], durations['PyPDFium2'] / durations['unPDF']
    ))
    print(f"  {'PyPDFium2 plaintext duration':<40}: {{:.4f}} ({{:.2f}}x) seconds".format(
        durations['Optimum'], durations['Optimum'] / durations['unPDF']
    ))