import os
from distutils.core import setup
from Cython.Build import cythonize

# Cython's version of Extension class for extra parameters to work:
from Cython.Distutils import build_ext, Extension

# setup_args = {'name': 'module', 'license': 'MIT', 'author': 'Mars',

# Relative not absolute path, OFC.
if "SETUP_PATH" in os.environ:
    raw_path = os.environ['SETUP_PATH']
else:
    raw_path = 'src/'

# @TODO: Iterate over src directory using utils function, obvi.
ext1 = Extension(name="jira_read_model", sources=['jira_read_model.py'])
ext2 = Extension(name="jira_write_model", sources=['jira_wite_model.py'])
sources=[ext1, ext2]

# ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError, IOError, SystemExit)

ext_modules=cythonize(sources,
    compiler_directives={'language_level' : "3"},
    build_dir='../../lib/c',
    annotate=False)

setup(
    # name = 'LoanInfo',
    ext_modules = ext_modules
)
