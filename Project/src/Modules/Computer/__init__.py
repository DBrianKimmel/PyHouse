"""
This is the computer package.

Things in this package are more closely related to the computer that PyHouse is running on than with the house itself.

This components of this package run before any of the house components.
"""

__updated__ = '2020-01-03'
__version_info__ = (20, 1, 3)
__version__ = '.'.join(map(str, __version_info__))

MODULES = [  # All modules for the computer must be listed here.  They will be loaded if configured.
    'Bridges',
    'Communication',
    'Internet',
    'Nodes',
    'Pi',
    # 'Weather',
    'Web'
    ]

PARTS = [
    ]

# ## END DBK
