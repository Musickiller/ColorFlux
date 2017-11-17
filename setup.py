# from distutils.core import setup
# import py2exe

# setup(windows=['ColorFlux.py'])

# import cx_Freeze

# exe = [cx_Freeze.Executable("ColorFlux.py")]

# cx_Freeze.setup( name = "ColorFlux", version = "1.0", options = {"build_exe": {"packages": ["errno", "os", "re", "stat", "subprocess","collections", "pprint","shutil", "humanize","pycallgraph"], "include_files": []}}, executables = exe )

###

# cx_Freeze.setup( name = "ColorFlux", version = "1.0", options = {"build_exe": {"packages": ["os", "pyglet", "random"], "include_files": []}}, executables = exe )


#########

build_exe_options = {"packages": ["pyglet"]}

from cx_Freeze import setup, Executable

import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

setup(
    name = "ColorFlux",
    version = "1.0",
    description = "test",
    options = {"build_exe":build_exe_options},
    executables = [Executable("ColorFlux.py")])