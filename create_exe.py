# Create Windows executable for packager using
# Py2Exe module - http://www.py2exe.org
# Usage: python create_exe.py py2exe
from distutils.core import setup
import py2exe

setup(
    options = {'py2exe': {'bundle_files': 1}},
    console = ['packager.py'],
    zipfile = None,
)
