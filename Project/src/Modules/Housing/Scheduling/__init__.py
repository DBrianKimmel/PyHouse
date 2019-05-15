"""
@name:      PyHouse/Project/src/Modules/Housing/Scheduling/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@note:      Created on April 8, 2013
@license:   MIT License
@summary:   Valid types

"""

__updated__ = '2019-05-12'
__version_info__ = (19, 5, 1)
__version__ = '.'.join(map(str, __version_info__))

VALID_SCHEDULING_TYPES = ['Lighting', 'Hvac', 'Irrigation', 'Pool', 'Entertainment' ]
VALID_SCHEDULE_MODES = ['Always', 'Home', 'Vacation', 'Away']

# ## END DBK
