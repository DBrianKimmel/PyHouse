"""
-*- test-case-name: PyHouse.src.Modules.Families.Insteon.test.test_Insteon_data -*-

@name: PyHouse/src/Modules/Families/Insteon/Insteon_data.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Aug 6, 2014
@summary: This module is for communicating with Insteon controllers.

"""

# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import LightData


class InsteonData (LightData):
    """This class contains the Insteon specific information about the various devices controlled by PyHouse.
    """
    def __init__(self):
        super(InsteonData, self).__init__()
        self.ControllerFamily = 'Insteon'
        self.DevCat = 0  # DevCat and SubCat (2 bytes)
        self.GroupList = ''
        self.GroupNumber = 0
        self.InsteonAddress = 0  # Long integer internally - '1A.B3.3C' for external reaability
        self.IsController = False
        self.IsMaster = False  # False is Slave
        self.IsResponder = False
        self.ProductKey = ''

# ## END DBK
