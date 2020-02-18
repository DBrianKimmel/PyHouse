"""
@name:      Modules/House/Lighting/Buttons/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2020-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Feb  5, 2020

"""

__updated__ = '2020-02-09'
__version_info__ = (20, 2, 9)
__version__ = '.'.join(map(str, __version_info__))

CONFIG_NAME = 'buttons'


class ButtonInformation:

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.DeviceType = 'Lighting'
        self.DeviceSubType = 'Button'
        self.Type = None  # Remote, Slave
        self.Family = None  # FamilyInformation()
        self.Room = None  # RoomInformation()
        self.Buttons = None

# ## END DBK
