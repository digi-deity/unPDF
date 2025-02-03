import tarfile
import sys
from platform import system, machine
import pathlib
import shutil

from Cython.Build import cythonize
from Cython.Distutils import build_ext
from setuptools import setup, Extension

is_64bits = sys.maxsize > 2**32

if system() == 'Windows':
    platform = 'win'
    runtime_library_dirs=[]
    libraries = ['pdfium.dll']
elif system() == 'Linux':
    platform = 'linux'
    libraries = ['pdfium']
    runtime_library_dirs=['$ORIGIN/']
else:
    raise SystemError("Unsupported system")

arch = 'x64' if is_64bits else 'x86'
arch = 'arm64' if 'arm' in machine() else arch

tgz = pathlib.Path(f'./lib/pdfium-{platform}-{arch}.tgz')
if tgz.exists():
    shutil.rmtree('./lib/pdfium/', ignore_errors=True)
    with tarfile.open(tgz, 'r:gz') as f:
        f.extractall('./lib/pdfium/')

    for p in ['./lib/pdfium/lib/libpdfium.so', './lib/pdfium/bin/pdfium.dll']:
        if pathlib.Path(p).exists():
            shutil.copy(p, './pdfextract/')

extensions = [
       Extension(
            'pdfextract.libpdf',
            sources=["pdfextract/libpdf.pyx"],
            libraries=libraries,
            runtime_library_dirs=runtime_library_dirs,
            library_dirs=['lib/pdfium/lib/'],
            include_dirs=['lib/pdfium/include/'],
       )
]

setup(
   cmdclass={"build_ext": build_ext},
   ext_modules=cythonize(extensions, compiler_directives={'language_level': "3str"}),
)