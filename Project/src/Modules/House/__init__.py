"""
@name:      Modules/House/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Handle all of the information for a house.

"""

__updated__ = '2020-02-16'
__version_info__ = (20, 2, 3)
__version__ = '.'.join(map(str, __version_info__))

# Note that the following are in the order needed to sequence the startup
MODULES = [  # All modules for the House must be listed here.  They will be loaded if configured.
    'Lighting',
    'Hvac',
    'Security',
    'Irrigation',
    'Pool',
    'Rules',
    'Schedule',
    'Sync',
    'Entertainment',
    'Family'
    ]

PARTS = [
    'Location',
    'Floors',
    'Rooms'
    ]

CONFIG_NAME = 'house'


class HouseInformation:
    """
    ==> PyHouse_obj.House.xxx
    """

    def __init__(self):
        self.Name: Union[str, None] = None
        self.Comment: str = ''
        self._Apis = {}


class LocationInformation:
    """ Location of the houses
    Latitude, Longitude and Elevation allow the computation of local sunrise and sunset
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
        self._RiseSet = None


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
