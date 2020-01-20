"""
@name:      Modules/families/UPB/UPB_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 6, 2014
@summary:   This module is for communicating with UPB controllers.

"""

__updated__ = '2020-01-20'

# Import system type stuff

# Import PyMh files
from Modules.House.Lighting.lights import LightControlInformation


class UPBData(LightControlInformation):
    """
    Locally held data about each of the UPB PIM controllers we find.

    This is known only within the UPB family package.
    """

    def __init__(self):
        super(UPBData, self).__init__()
        self.UPBAddress = 0
        self.UPBPassword = 0
        self.UPBNetworkID = 0

# ## END DBK
