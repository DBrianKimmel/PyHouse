"""
@name:      Modules/House/house_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 16, 2019
@summary:   All of the information for a house.

PyHouse.House.
              Location
              Rooms
"""

__updated__ = '2019-10-16'
__version_info__ = (19, 6, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
from typing import Any

#  Import PyMh files
from Modules.Core.data_objects import BaseUUIDObject, RiseSetData
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.House_data     ')


class LocationInformation:
    """ Location of the houses
    Latitude and Longitude allow the computation of local sunrise and sunset
    """

    def __init__(self):
        self.Street = None
        self.City = None
        self.State = None
        self.ZipCode = None
        self.Country = None
        self.Phone = None
        self.Latitude = None
        self.Longitude = None
        self.Elevation = None
        self.TimeZone = None


class CoordinateInformation:
    """
    If applied to components of a house (facing the 'Front' of a house:
        X or the distance to the Right from the room's Left side.
        Y or the distance back from the Front of the room.
        Z or the Height above the floor.
    Preferably the distance is kept in Meters but for you die hard Imperial measurement people in Decimal feet (no inches)!

    In case you need some hints:
        Light switches are about 1.0 meters above the floor.
        Outlets are about 0.2 meters above the floor.
    """

    def __init__(self):
        self.X_Easting = 0.0
        self.Y_Northing = 0.0
        self.Z_Height = 0.0

# ## END DBK

