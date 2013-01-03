"""
main.__init__.py

The main core of PyHouse.

The core is starts as root and becomes user pyhouse and group pyhouse.
Be sure that user pyhouse is also in group dialout so we can access the controllers.

"""

__version_info__ = (1, 1, 0)
__version__ = '.'.join(map(str, __version_info__))


# ## END
