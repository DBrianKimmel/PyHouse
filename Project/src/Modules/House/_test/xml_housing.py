"""
@name:      PyHouse/src/Modules/Housing/_test/xml_housing.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 7, 2014
@summary:   XML data for house location

See PyHouse/src/_test/xml_data.py for the entire hierarchy.

Here is the description of the various configuration entries.

RoomName is the location of the device we are describing.  This could be something other than
a room in the house such as front lawn, pool LivingRoom and so on.

Coords are the X, Y and Z offsets within the room for the device.

Comments should not need explaining.  They are just present and can contain just about anything.
"""
from Modules.Housing.Rules.test.xml_rules import XML_RULES_SECTION

__updated__ = '2019-07-29'

# Import system type stuff

# Import PyMh files
from Modules.Housing.test.xml_location import XML_LOCATION
from Modules.Housing.test.xml_rooms import XML_ROOMS
from Modules.Housing.Entertainment.test.xml_entertainment import XML_ENTERTAINMENT
from Modules.Housing.Hvac.test.xml_hvac import XML_HVAC
from Modules.Housing.Irrigation.test.xml_irrigation import XML_IRRIGATION
from Modules.Housing.Lighting.test.xml_lighting import XML_LIGHTING
from Modules.Housing.Pool.test.xml_pool import XML_POOL
from Modules.Housing.Schedules.test.xml_schedule import XML_SCHEDULE
from Modules.Housing.Security.test.xml_security import XML_SECURITY

TESTING_HOUSE_DIVISION = 'HouseDivision'

TESTING_HOUSE_NAME = 'Pink Poppy'
TESTING_HOUSE_KEY = '0'
TESTING_HOUSE_ACTIVE = 'True'
TESTING_HOUSE_UUID = 'House...-0000-0000-0000-333e5f8cdfd2'
TESTING_HOUSE_COMMENT = 'House on Pink Poppy Drive'
TESTING_HOUSE_MODE = 'Home'
TESTING_HOUSE_PRIORITY = '5'

L_HOUSE_DIV = '<' + TESTING_HOUSE_DIVISION + \
        " Name='" + TESTING_HOUSE_NAME + \
        "' Key='" + TESTING_HOUSE_KEY + \
        "' Active='" + TESTING_HOUSE_ACTIVE + \
        "'>"
L_HOUSE_UUID = '<UUID>' + TESTING_HOUSE_UUID + '</UUID>'
L_HOUSE_COMMENT = '<Comment>' + TESTING_HOUSE_COMMENT + '</Comment>'
L_HOUSE_MODE = "<Mode>" + TESTING_HOUSE_MODE + "</Mode>"
L_HOUSE_PRIORITY = '<Priority>' + TESTING_HOUSE_PRIORITY + '</Priority>'

L_HOUSE_DIVISION_END = '</' + TESTING_HOUSE_DIVISION + '>'

XML_HOUSE_DIVISION = '\n'.join([
    L_HOUSE_DIV,
    L_HOUSE_UUID,
    L_HOUSE_COMMENT,
    L_HOUSE_MODE,
    L_HOUSE_PRIORITY,
    XML_LOCATION,
    XML_ROOMS,
    XML_LIGHTING,
    XML_HVAC,
    XML_ENTERTAINMENT,
    XML_IRRIGATION,
    XML_POOL,
    XML_RULES_SECTION,
    XML_SCHEDULE,
    XML_SECURITY,
    L_HOUSE_DIVISION_END
])

# ## END DBK
