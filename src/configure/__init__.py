"""
# configure/__init__.py

This package is required for PyHouse.

It will use XML to read/store the configuration.

Major subsections will have an active flag set to true if they are used.
If a section is not used it will be preserved and the active flag will be
 set to false.

Example of XML file

<PyHouse>
    <Houses Active=true>
        <House Name=name Key=1 Active=true>
            <Location>
                ...
            </location>
            <Rooms>
                <Room Name=name Key=1 Active=true>
                    ...
                </Room>

"""

import sys

__version_info__ = (0, 1, 4)
__version__ = '.'.join(map(str, __version_info__))

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
