"""
# insteon/__init__.py

This interfaces PyHouse to the Insteon family of products.
This includes light switches, thermostats and a number of other devices.


"""

import sys

__version_info__ = (1, 0, 2)
__version__ = '.'.join(map(str, __version_info__))

try:
    from twisted import version as twisted_version
    from twisted.web import version as twisted_web_version
    from twisted.python.versions import Version
except ImportError, exc:
    # log error to stderr, might be useful for debugging purpose
    sys.stderr.write("Twisted >= 2.5 and Twisted.Web >= 2.5 are required. "\
                     "Please install them.\n")
    raise

#print "families.insteon.__init__.py ", twisted_version

import Device_Insteon
import Insteon_PLM

### END#
