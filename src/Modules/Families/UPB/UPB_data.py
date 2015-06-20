"""
-*- test-case-name: PyHouse.src.Modules.families.UPB.test.test_UPB_data -*-

@name:      PyHouse/src/Modules/families/UPB/UPB_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 6, 2014
@summary:   This module is for communicating with UPB controllers.

"""

# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import LightData


class UPBData(LightData):
    """
    Locally held data about each of the UPB PIM controllers we find.

    This is known only within the UPB family package.
    """

    def __init__(self):
        super(UPBData, self).__init__()
        self.ControllerFamily = 'UPB'
        self.UPBAddress = 0
        self.UPBPassword = 0
        self.UPBNetworkID = 0

# ## END DBK
