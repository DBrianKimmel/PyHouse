"""
@name:      Modules/House/Lighting/Controllers/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2020-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Feb  8, 2020

"""

__updated__ = '2020-02-08'
__version_info__ = (20, 2, 8)
__version__ = '.'.join(map(str, __version_info__))

CONFIG_NAME = 'controllers'


class ControllerInformation:
    """
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.DeviceType = 'Lighting'
        self.DeviceSubType = 'Controller'
        self.Family = None
        self.Interface = None  # Interface module specific  DriverInterfaceInformation()
        self.Access = None  # Optional ==> AccessInformation()
        self.LinkList = {}
        #
        self._Message = bytearray()
        self._Queue = None
        self._isLocal = False
        self.Room = None  # RoomInformation()

# ## END DBK
