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
from Modules.Housing.test.xml_location import LOCATION_XML
from Modules.Housing.test.xml_rooms import ROOMS_XML
from Modules.Scheduling.test.xml_schedule import SCHEDULE_XML
from Modules.Lighting.test.xml_lighting import LIGHTING_XML, LIGHTING_XML_1_3
from Modules.Hvac.test.xml_thermostat import XML_THERMOSTAT
from Modules.Entertainment.test.xml_entertainment import ENTERTAINMENT_XML
from Modules.Irrigation.test.xml_irrigation import IRRIGATION_XML


HOUSE_DIVISION_XML = '\n'.join([
    "<HouseDivision Name='Pink Poppy' Key='0' Active='True'>",
    "    <UUID>12345678-1002-11e3-b583-333e5f8cdfd2</UUID>",
    LOCATION_XML,
    ROOMS_XML,
    SCHEDULE_XML,
    LIGHTING_XML,
    XML_THERMOSTAT,
    ENTERTAINMENT_XML,
    IRRIGATION_XML,
    "</HouseDivision>"
])

HOUSE_DIVISION_XML_1_3 = '\n'.join([
    "<HouseDivision Name='Pink Poppy' Key='0' Active='True'>",
    "    <UUID>12345678-1002-11e3-b583-333e5f8cdfd2</UUID>",
    LOCATION_XML,
    ROOMS_XML,
    SCHEDULE_XML,
    LIGHTING_XML_1_3,
    XML_THERMOSTAT,
    ENTERTAINMENT_XML,
    IRRIGATION_XML,
    "</HouseDivision>"
])

# ## END DBK
