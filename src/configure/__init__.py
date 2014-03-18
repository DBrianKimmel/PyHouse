"""
# configure/__init__.py

This package is required for PyHouse.

It will use XML to read/store the configuration.

There is a skeleton config file in /etc named pyhouse.conf
The only purpose of this file is to set up the location of the full config file
which is updated by the PyHouse daemon after it has given up root permissions.

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

__version_info__ = (1, 1, 0)
__version__ = '.'.join(map(str, __version_info__))

try:
    from Tkinter import TkVersion as tk_version
except ImportError, exc:
    import sys
    sys.stderr.write("Tkinter is required.  Please install it.\n")
    raise

# ## END DBK
