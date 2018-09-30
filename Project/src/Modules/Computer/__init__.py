"""
This is the computer package.

Things in this package are more closely related to the computer that PyHouse is running on than with the
house itself.

This components of this package run before any of the house components.
"""

__updated__ = '2017-01-19'
__version_info__ = (1, 7, 5)
__version__ = '.'.join(map(str, __version_info__))

VALID_COMPUTER_MODULES = ['Communication', 'Internet', 'Mqtt', 'Nodes', 'Pi', 'Weather', 'Web']

# ## END DBK
