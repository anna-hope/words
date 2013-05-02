from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("get_freqs", ["get_freqs.pyx"])]

setup(
  name = 'Get frequencies of sequences in a bank of sequnces',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)