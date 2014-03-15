"""Developer documentation.

Most of the developer documentation is in each package __init__.py module.

Overall documentation.

Each module will most likely contain an 'API' class.  The constructor for
this class will give a reference address for the module.

The 'Start' method will read any XML and set up the data for this
module.  It will also call any other modules that it will need.

The 'Stop' method will write any XML file to update it.  It will also
close down any thing it no longer needs so they can be cleanly reloaded.

In order to keep the API class clean, modules may have a 'Utilities'
class.  The API class will inherit from this class so that its
methods may be accessible by other modules.

The PyHouse module created a data structure that is passed to some
high level modules.

o logs
g_debug
0 = no console output, log err, warn & info
1 = no console output, log extra info messages
"""

__version_info__ = (1, 1, 0)
__version__ = '.'.join(map(str, __version_info__))

# ## END DBK
