"""
@name:      PyHouse/src/Modules/Housing/test/xml_housing.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
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

__updated__ = '2016-07-07'

# Import system type stuff

# Import PyMh files
from Modules.Housing.test.xml_location import XML_LOCATION
from Modules.Housing.test.xml_rooms import XML_ROOMS
from Modules.Scheduling.test.xml_schedule import XML_SCHEDULE
from Modules.Lighting.test.xml_lighting import XML_LIGHTING
from Modules.Hvac.test.xml_hvac import XML_HVAC
from Modules.Entertainment.test.xml_entertainment import XML_ENTERTAINMENT
from Modules.Irrigation.test.xml_irrigation import XML_IRRIGATION
from Modules.Pool.test.xml_pool import XML_POOL


TESTING_HOUSE_NAME = 'Pink Poppy'
TESTING_HOUSE_KEY = '0'
TESTING_HOUSE_ACTIVE = 'True'
TESTING_HOUSE_UUID = 'House...-0000-0000-0000-333e5f8cdfd2'

L_HOUSE_DIV = "<HouseDivision Name='" + TESTING_HOUSE_NAME + \
            "' Key='" + TESTING_HOUSE_KEY + \
            "' Active='" + TESTING_HOUSE_ACTIVE + \
            "'>"
L_HOUSE_UUID = '<UUID>' + TESTING_HOUSE_UUID + '</UUID>'

L_HOUSE_DIVISION_END = '</HouseDivision>'

HOUSE_DIVISION_XML = '\n'.join([
    L_HOUSE_DIV,
    L_HOUSE_UUID,
    XML_LOCATION,
    XML_ROOMS,
    XML_SCHEDULE,
    XML_LIGHTING,
    XML_HVAC,
    XML_ENTERTAINMENT,
    XML_IRRIGATION,
    XML_POOL,
    L_HOUSE_DIVISION_END
])

# ## END DBK
