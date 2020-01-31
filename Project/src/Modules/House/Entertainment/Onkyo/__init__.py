"""
@name:      Modules/House/Entertainment/Onkyo/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c)2016-2020 by D. Brian Kimmel
@note:      Created on Jul 9, 2016
@license:   MIT License
"""

__updated__ = '2020-01-28'
__version_info__ = (20, 1, 26)
__version__ = '.'.join(map(str, __version_info__))

from Modules.House.Entertainment import EntertainmentPluginInformation, EntertainmentDeviceInformation, EntertainmentDeviceControl, EntertainmentDeviceStatus


class OnkyoPluginInformation(EntertainmentPluginInformation):
    """
    """

    def __init__(self):
        super(OnkyoPluginInformation, self).__init__()


class OnkyoDeviceInformation(EntertainmentDeviceInformation):
    """ A super that contains some onkyo specific fields
    """

    def __init__(self):
        super(OnkyoDeviceInformation, self).__init__()
        self.Commands = None
        self.Type = None
        self.Volume = None
        self.Zone = None


class OnkyoDeviceControl(EntertainmentDeviceControl):
    """ Used to control a device.
    All defaults are None - Only fill in what you need so inadvertent controls are not done.
    """

    def __init__(self):
        super(OnkyoDeviceControl, self).__init__()
        pass


class OnkyoDeviceStatus(EntertainmentDeviceStatus):
    """
    The device family is part of the topic.
    """

    def __init__(self):
        super(OnkyoDeviceStatus, self).__init__()
        pass

# ## END DBK
