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

DIR = pathlib.Path(__file__).parent.resolve(strict=False)

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

arch = 'x64'
arch = 'arm64' if (is_arm or platform == 'mac')  else arch
musl = '-musl' if is_musl else ''

pdfium_lib_dir = DIR / 'lib'
tgz = pdfium_lib_dir / f'pdfium-{platform}{musl}-{arch}.tgz'

print(f"Detected platform: {platform}, architecture: {arch}, musl: {bool(musl)}")
print(f"Looking for PDFium distribution at: {tgz}")

if tgz.exists():
    shutil.rmtree(pdfium_lib_dir / 'pdfium', ignore_errors=True)
    with tarfile.open(tgz, 'r:gz') as f:
        f.extractall(pdfium_lib_dir / 'pdfium')

    for p in [
        pdfium_lib_dir / 'pdfium' / 'lib' / 'libpdfium.so',
        pdfium_lib_dir / 'pdfium' / 'bin' / 'pdfium.dll',
        pdfium_lib_dir / 'pdfium' / 'lib' / 'libpdfium.dylib',
    ]:
        if pathlib.Path(p).exists():
            shutil.copy(p, 'pdf_extract/')
            break
    else:
        print(f"PDFium library not found in the expected locations: Please confirm extraction.")
else:
    print(f"Expected PDFium distribution at {tgz}. Please make sure it exists in the 'lib' directory.")

if not pathlib.Path('./lib/pdfium').exists():
    raise FileNotFoundError(f"PDFium distribution not found. Please download and extract it to './lib/pdfium/'")

extensions = [
       Extension(
            'pdf_extract.libpdf',
            sources=["pdf_extract/libpdf.pyx"],
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