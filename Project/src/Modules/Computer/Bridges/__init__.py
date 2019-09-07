"""
@name:      PyHouse/src/Modules/Computers/Bridgess/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Dec 21, 2017
@license:   MIT License
@summary:

The Bridges  module is where the external bridge or hub type devices are defined.

Examples:
    Insteon Hub (or bridge)
    Philips Hue Hub (or bridge)

"""

__updated__ = '2019-05-12'
__version_info__ = (19, 5, 0)
__version__ = '.'.join(map(str, __version_info__))

VALID_BRIDGE_TYPES = ['Null', 'Insteon', 'Hue', 'Weather']

# ## END DBK
