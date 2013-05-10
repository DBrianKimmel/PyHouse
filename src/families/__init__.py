"""
families.__init__.py

Various families of lighting systems.

insteon
upb
x-10
zigbee
z-wave
lutron
and others

To add a family named 'NewFamily', do the following:
    * Add a package named 'New_Family'.
    * Add the family name (Capitalized) to the list VALID_FAMILIES below.
    * Add a module named Device_<NewFamily>.py
    * Add any other modules needed by the Device module.
    * A module to interface with the controller is recommended.

There are a number of lighting 'Family' types handled here.
The Insteon family is now functional (2012).
The UPB family is work in progress
The X-10 family is mostly just a stub at present (2012)

Each family consists of four major areas:
    Lights / Lighting Devices
    Controllers - connected to the computer
    Scenes - have one or more lights that are controlled together
    Buttons - extra buttons with no light directly attached (key-pad-link)

"""

__version_info__ = (1, 0, 0)
__version__ = '.'.join(map(str, __version_info__))

VALID_FAMILIES = ['Insteon', 'UPB', 'X10']

import importlib

for l_family in VALID_FAMILIES:
    l_package = 'families.' + l_family
    l_import = 'Device_' + l_family
    l_module = l_package + '.' + l_import
    # print "families() from {0:} import {1:} -- Module:{2:}".format(l_package, l_import, l_module)
    try:
        l_module = importlib.import_module(l_module, l_package)
    except ImportError:
        # print "\nfamilies.__init__() - ImportError: Family:'{0:}', Name:'{1:}', Package:'{2:}'.\n".format(l_family, l_import, l_package)
        pass

# ## END
