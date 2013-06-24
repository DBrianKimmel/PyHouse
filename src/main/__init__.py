"""
main.__init__.py

The main core of PyHouse.

The core modules start as root and become user pyhouse and group pyhouse.
Be sure that user pyhouse is also in group dialout so we can access the controllers.

The main group of python modules start the entire PyHouse suite and provide
a core of tools and modules that are always present.

Houses is a core module that will instantiates 'house' for every house defined
to operate via PyHouse.  That is in the configuration XML file.

During development this is run by hand.
It is, however, planned to be a daemon that is kicked off on system start-up.
It is intended to run on everything from a small, low power bare bones system
to a server running multiple houses in several, widespread locations.

The system is controlled in several ways.
One is via a browser connecting to a web server that will
be either integrated or separate from PyHouse.
Another is via an integrated GUI.

The highest level is the House/Location.  Every house has a location and
contains a number of rooms.
Each house must be unique and its name is used to qualify lower level rooms
and devices.

Each house will have a schedule that is only for that house.
Each house will need at least a small bare bone system to control all the serial, USB,
and Ethernet devices used to control the various devices in the house.

The next level is the room.  Rooms may be duplicated between houses but must
be unique within a single house.  Therefore you may not have 3 bedrooms named
'bedroom' and so on.

Python modules used:
    Core python 2.7
    Twisted
    zope.interface
    nevow
    PySerial
    PyUsb
    ConfigObj
    Pmw


for a raspberry-pi with wheezy:
debian (apt-get):
    python-twisted
    python-pmw
    python coherence



also install:
    libusb

Modules desired are:
    Web server - allow control over the Internet by a browser
    Scheduler - kick off automation that follows a schedule
    Lighting - allow automation of home lighting systems
    Heating,
    Pool Control.
    Irrigation control.
    Entertainment - allow control of tv, video systems, audio systems etc
    Surveillance - allow remote control of video cameras etc.
"""

__version_info__ = (1, 1, 0)
__version__ = '.'.join(map(str, __version_info__))

# ## END DBK
