"""
@name:      Modules/Lighting/lighting_buttons.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2019 by D. Brian Kimmel
@note:      Created on Apr 2, 2010
@license:   MIT License
@summary:   Handle the home lighting system automation.

"""

__updated__ = '2019-07-30'

#  Import system type stuff

#  Import PyHouse files

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.LightingButton ')


class ButtonInformation:

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.DeviceType = 'Lighting'
        self.DeviceSubType = 'Button'
        self.Family = None  # FamilyInformation()
        # self.DeviceType = 0  # 'Lighting = Controllers, 1 = Lighting, 2 = HVAC, 3 = Security, 4 = Bridge
        # self.DeviceSubType = 'Button'
        # self.Location = None  # RoomLocationInformation()


class Config:
    """
    """


class API:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def LoadConfig(self):
        """
        """

    def SaveConfig(self):
        """
        """

#  ## END DBK
