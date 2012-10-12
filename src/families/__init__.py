"""
families.__init__.py

Various families of lighting systems.

insteon
upb
x-10
zigbee
z-wave
and others

To add a family do the following:
    * Add a package named family.
    * Add the family name (Capitalized) to VALID_FAMILIES below.
    * Add a module named Device_<Family>.py
    * Add any other modules needed by the Device module.
    * A module to interface with the controller is recommended.

"""

__version_info__ = (1, 0, 0)
__version__ = '.'.join(map(str, __version_info__))

VALID_FAMILIES = ['Insteon', 'UPB', 'X10']

import importlib
try:
    for l_family in VALID_FAMILIES:
        l_name = 'Device_' + l_family
        l_package = 'families.' + l_family
        #print "families.__init__.py - Family:{0:}, Name:{1}, Package:{2:}".format(l_family, l_name, l_package)
        l_module = importlib.import_module(l_package, l_family)
except ImportError:
    print "Error - Package missing from families."

### END
