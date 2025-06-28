import tarfile
import sys
from platform import system, machine, uname
import pathlib
import shutil
import os
import sysconfig

from Cython.Build import cythonize
from Cython.Distutils import build_ext
from setuptools import setup, Extension

suffix = os.environ.get('SETUPTOOLS_EXT_SUFFIX', sysconfig.get_config_vars()['EXT_SUFFIX'])
print(f"Extension suffix: {suffix}")

is_64bits = sys.maxsize > 2**32
is_arm = ('arm' in suffix or 'aarch64' in suffix)
is_musl = 'musl' in suffix

if system() == 'Windows':
    platform = 'win'
    runtime_library_dirs=[]
    libraries = ['pdfium.dll']
elif system() == 'Linux':
    platform = 'linux'
    libraries = ['pdfium']
    runtime_library_dirs=['$ORIGIN/']
elif system() == 'Darwin':
    platform = 'mac'
    libraries = ['pdfium']
    runtime_library_dirs=[]
else:
    raise SystemError("Unsupported system")

arch = 'x64' if is_64bits else 'x86'
arch = 'arm64' if is_arm else arch
musl = '-musl' if is_musl else ''

tgz = pathlib.Path(f'./lib/pdfium-{platform}{musl}-{arch}.tgz')

if tgz.exists():
    shutil.rmtree('./lib/pdfium/', ignore_errors=True)
    with tarfile.open(tgz, 'r:gz') as f:
        f.extractall('./lib/pdfium/')

    for p in ['./lib/pdfium/lib/libpdfium.so', './lib/pdfium/bin/pdfium.dll']:
        if pathlib.Path(p).exists():
            shutil.copy(p, './pdfextract/')

if not pathlib.Path('./lib/pdfium').exists():
    raise FileNotFoundError(f"PDFium distribution not found. Please download and extract it to './lib/pdfium/'")

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