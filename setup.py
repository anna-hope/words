#!/usr/bin/env python3.3

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("langtools", ["langtools.pyx"])]

setup(
  name = 'langtools',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)