"""
@name:      PyHouse/src/Modules/Housing/Scheduling/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2017 by D. Brian Kimmel
@note:      Created on April 8, 2013
@license:   MIT License
@summary:   Valid types


# schedule/__init__.py

This is one of the major components of PyHouse.

"""

__updated__ = '2016-08-18'
__version_info__ = (1, 6, 1)
__version__ = '.'.join(map(str, __version_info__))

VALID_SCHEDULING_TYPES = ['Lighting', 'Hvac', 'Irrigation', 'Pool', 'Entertainment' ]
VALID_SCHEDULE_MODES = ['Always', 'Home', 'Vacation', 'Away']

# ## END DBK
