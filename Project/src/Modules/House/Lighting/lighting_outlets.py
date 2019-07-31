'''
Created on Jul 18, 2019

@author: briank
'''
"""
@name:      Modules/Housing/Lighting/lighting_outlets.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@note:      Created on Jul 18, 2019
@license:   MIT License
@summary:   Handle the home lighting system automation.


"""

__updated__ = '2019-07-24'

#  Import system type stuff

#  Import PyMh files and modules.

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.OutletControl  ')

CONFIG_FILE_NAME = 'outlets.yaml'


class OutletInformation:
    """ This is the information that the user needs to enter to uniquely define a Outlet.
    """

    def __init__(self):
        self.Name = None
        self.Comment = None  # Optional
        self.DeviceType = 'Lighting'
        self.DeviceSubType = 'Outlet'
        self.LastUpdate = None  # Not user entered but maintained
        self.Uuid = None  # Not user entered but maintained
        self.Family = None  # LightFamilyInformation()
        self.Room = None  # LightRoomInformation() Optional


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

# ## END DBK
