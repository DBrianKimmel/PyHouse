"""
@name:      Modules/House/Entertainment/Samsung/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2020 by D. Brian Kimmel
@note:      Created on Jul 11, 2016
@license:   MIT License
"""

__updated__ = '2020-01-28'
__version_info__ = (20, 1, 26)
__version__ = '.'.join(map(str, __version_info__))

from Modules.House.Entertainment import \
    EntertainmentPluginInformation, EntertainmentDeviceInformation


class SamsungPluginInformation(EntertainmentPluginInformation):
    """
    """

    def __init__(self):
        super(SamsungPluginInformation, self).__init__()


class SamsungDeviceInformation(EntertainmentDeviceInformation):
    """ A superset that contains some samsung specific fields
    """

    def __init__(self):
        super(SamsungDeviceInformation, self).__init__()
        self.Room = None
        self.Type = None
        self.Volume = None

# ## END DBK
