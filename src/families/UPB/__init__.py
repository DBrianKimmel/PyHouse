#
# upb/__init__.py
#

import sys

__version_info__ = (0,1,8)
__version__ = '.'.join(map(str,__version_info__))

try:
    from twisted import version as twisted_version
except ImportError, exc:
    # log error to stderr, might be useful for debugging purpose
    sys.stderr.write("Twisted >= 2.5 is required.  Please install it.\n")
    raise

print twisted_version

### END