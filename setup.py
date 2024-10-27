from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

cythonized = cythonize(
   [
       Extension(
            '*',
            sources=["src/charminator/**/*.pyx"],
            libraries=['pdfium'],
            runtime_library_dirs=['lib/'],
            library_dirs=['lib/'],
            include_dirs=['lib/'],
       )
   ],
compiler_directives={'language_level': "3str"},
annotate=True,
)


setup(
   name='project',
   packages=find_packages(where='src'),
   package_dir={'': 'src'},
   ext_modules=cythonized
)