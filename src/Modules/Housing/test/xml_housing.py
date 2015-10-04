"""
@name:      PyHouse/src/Modules/Housing/test/xml_housing.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 7, 2014
@summary:   XML data for house location

See PyHouse/src/test/xml_data.py for the entire hierarchy.

Here is the description of the various configuration entries.

RoomName is the location of the device we are describing.  This could be something other than
a room in the house such as front lawn, pool LivingRoom and so on.

Coords are the X, Y and Z offsets within the room for the device.

Comments should not need explaining.  They are just present and can contain just about anything.
"""

# Import system type stuff

# Import PyMh files
from Modules.Housing.test.xml_location import XML_LOCATION
from Modules.Housing.test.xml_rooms import XML_ROOMS
from Modules.Scheduling.test.xml_schedule import XML_SCHEDULE
from Modules.Lighting.test.xml_lighting import XML_LIGHTING
from Modules.Hvac.test.xml_hvac import XML_HVAC
from Modules.Entertainment.test.xml_entertainment import ENTERTAINMENT_XML
from Modules.Irrigation.test.xml_irrigation import XML_IRRIGATION
from Modules.Pool.test.xml_pool import XML_POOL


TESTING_HOUSE_NAME = 'Pink Poppy'
TESTING_HOUSE_KEY = '0'
TESTING_HOUSE_ACTIVE = 'True'

L_HOUSE_DIV = "<HouseDivision Name='" + TESTING_HOUSE_NAME + "' Key='" + TESTING_HOUSE_KEY + "' Active='" + TESTING_HOUSE_ACTIVE + "'>"

HOUSE_DIVISION_XML = '\n'.join([
    L_HOUSE_DIV,
    "    <UUID>12345678-1002-11e3-b583-333e5f8cdfd2</UUID>",
    XML_LOCATION,
    XML_ROOMS,
    XML_SCHEDULE,
    XML_LIGHTING,
    XML_HVAC,
    ENTERTAINMENT_XML,
    XML_IRRIGATION,
    XML_POOL,
    "</HouseDivision>"
])

# ## END DBK
