"""
-*- test-case-name: PyHouse.src.Modules.Families.Insteon.test.test_Insteon_data -*-

@name:      PyHouse/src/Modules/Families/Insteon/Insteon_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 6, 2014
@summary:   This module contains data definition for Insteon devices.

"""

# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import LightData


class InsteonData(object):
    def __init__(self):
        self.DeviceFamily = 'Insteon'
        self.DevCat = 0  # DevCat and SubCat (2 bytes)
        self.EngineID = 0
        self.GroupList = ''
        self.GroupNumber = 0
        self.InsteonAddress = 0  # Long integer internally - '1A.B3.3C' for external reaability
        self.IsController = False
        self.IsMaster = False  # False is Slave
        self.IsResponder = False
        self.ProductKey = ''
        self.Version = 1  # the version of this data object.

# ## END DBK
