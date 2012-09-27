#
# configure/__init__.py
#

import sys

__version_info__ = (0,1,4)
__version__ = '.'.join(map(str,__version_info__))

try:
    from Tkinter import TkVersion as tk_version
except ImportError, exc:
    sys.stderr.write("Tkinter is required.  Please install it.\n")
    raise

import config_xml
import xml_tools
import gui
import gui_logs
import gui_house
import gui_schedule
import gui_lighting
import gui_web

### END