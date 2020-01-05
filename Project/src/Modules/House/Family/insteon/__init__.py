"""
@name:      Modules/House/Family/Insteon/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2020 by D. Brian Kimmel
@note:      Created on Apr 3, 2011
@license:   MIT License
@summary:   This module is for Insteon

This interfaces PyHouse to the Insteon family of products.
This includes light switches, thermostats and a number of other devices.
"""

__updated__ = '2020-01-03'
__version_info__ = (20, 1, 3)
__version__ = '.'.join(map(str, __version_info__))

MODULES = [
    'Lighting',
    'Hvac',
    'Security'
    ]

# ## END DBK
