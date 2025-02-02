from platform import system

from Cython.Build import cythonize
from Cython.Distutils import build_ext
from setuptools import setup, Extension

if system() == 'Windows':
    runtime_library_dirs=[]
    libraries = ['pdfium.dll']
elif system() == 'Linux':
    libraries = ['pdfium']
    runtime_library_dirs=['$ORIGIN/']
else:
    raise SystemError("Unsupported system")

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