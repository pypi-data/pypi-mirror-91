from setuptools import setup
from Cython.Build import cythonize
from os import getcwd
from os.path import join, dirname
import sys

def compile():
    include = [
        getcwd()
    ]


    setup(
        name="jpe_types.utils",
        ext_modules = cythonize(join(dirname(__file__), "subScripts.pyx"), 
                                annotate=True),
        include_dirs=include
    )

    # python36 build.py build_ext --inplace

compile()