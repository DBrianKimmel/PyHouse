"""
@name:       PyHouse/src/Modules.Core.Utilities.coordinate_tools.py
@author:     D. Brian Kimmel
@contact:    d.briankimmel@gmail.com
@copyright:  2016-2019 by D. Brian Kimmel
@date:       Created on Jun 21, 2016
@licencse:   MIT License
@summary:    Handle X,Y,Z coordinates

"""

__updated__ = '2019-07-15'

#  Import system type stuff
# import xml.etree.ElementTree as ET
# import datetime

#  Import PyMh files
from Modules.Housing.house_data import CoordinateInformation


class Coords:
    """
    """

    @staticmethod
    def _get_coords(p_coords):
        """ get CordinateData() from JSON data returned from the browser

        @param p_str: Json returns a list of X, Y and Z values.
                        It should look like >> [ 1, 2.2, 33.44 ] but it could be deformed by the user.
        @return: a CoordinateInformation() object filled in.
        """
        l_ret = CoordinateInformation()
        if isinstance(p_coords, list):
            l_list = p_coords
        else:
            l_list = p_coords.strip('\[\]')
            l_list = l_list.split(',')
        try:
            l_ret.X_Easting = float(l_list[0])
            l_ret.Y_Northing = float(l_list[1])
            l_ret.Z_Height = float(l_list[2])
        except Exception as e_err:
            print('Error {}'.format(e_err))
            l_ret.X_Easting = 0.0
            l_ret.Y_Northing = 0.0
            l_ret.Z_Height = 0.0
        return l_ret

# ## END DBK
