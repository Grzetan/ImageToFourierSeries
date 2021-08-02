from distutils.core import Extension, setup
from Cython.Build import cythonize
import numpy as np

ext = Extension(name="helper", sources=["functions/helper.pyx"], include_dirs=[np.get_include()])
setup(ext_modules=cythonize(ext))