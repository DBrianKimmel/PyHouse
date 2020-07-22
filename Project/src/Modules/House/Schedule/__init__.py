"""
@name:      Modules/House/Schedules/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2020 by D. Brian Kimmel
@note:      Created on April 8, 2013
@license:   MIT License
@summary:   Valid types

"""

__updated__ = '2020-02-04'
__version_info__ = (20, 2, 4)
__version__ = '.'.join(map(str, __version_info__))

VALID_SCHEDULE_MODES = ['Always', 'Home', 'Vacation', 'Away']


class ScheduleInformation:
    """ This is the basic schedule info
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.DOW = 'SMTWTFS'  # DayOfWeek - a dash '-' replaces the day letter if NOT that day
        self.Occupancy = 'Always'  # Always, Home, Away, Vacation, ...
        self.Time = None
        self.Sched = None  # One of the schedule detail types below.


class RiseSetInformation:
    """
    """

    def __init__(self):
        self.Dawn = 0
        self.SunRise = 0
        self.Noon = 0
        self.SunSet = 0
        self.Dusk = 0

# ## END DBK
