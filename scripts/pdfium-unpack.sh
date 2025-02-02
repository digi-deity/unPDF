#!/bin/bash

# Unpacks the PDFium source code and libraries.
# This script is intended to be run from the root of the project.

rm -rf lib/pdfium
mkdir lib/pdfium
tar -xzf lib/pdfium-${OS}.tgz -C lib/pdfium

# Copy the PDFium libraries to the pdfextract directory, if the bin directory exists
[[ -e lib/pdfium/bin/pdfium.dll ]] && cp lib/pdfium/bin/pdfium.dll pdfextract/
[[ -e lib/pdfium/lib/libpdfium.so ]] && cp lib/pdfium/lib/libpdfium.so pdfextract/