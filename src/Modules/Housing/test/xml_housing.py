"""
@name: C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/Housing/test/xml_location.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Nov 7, 2014
@Summary: XML data for house location

Here is the description of the various configuration entries.

RoomName is the location of the device we are describing.  This could be something other than
a room in the house such as front lawn, pool LivingRoom and so on.

Coords are the X and Y offsets within the room for the device.

Comments should not need explaining.  They are just present and can contain just about anything.
"""

# Import system type stuff

# Import PyMh files
from Modules.Housing.test.xml_location import LOCATION_XML
from Modules.Housing.test.xml_rooms import ROOMS_XML
from Modules.Scheduling.test.xml_schedule import SCHEDULE_XML
from Modules.Lighting.test.xml_lighting import LIGHTING_XML
from Modules.Hvac.test.xml_thermostat import THERMOSTAT_XML
from Modules.Entertainment.test.xml_entertainment import ENTERTAINMENT_XML



HOUSE_DIVISION_XML = '\n'.join([
    "<HouseDivision Name='Pink Poppy' Key='0' Active='True'>",
    "    <UUID>12345678-1002-11e3-b583-333e5f8cdfd2</UUID>",
    LOCATION_XML,
    ROOMS_XML,
    SCHEDULE_XML,
    LIGHTING_XML,
    THERMOSTAT_XML,
    ENTERTAINMENT_XML,
    "</HouseDivision>"
])

# ## END DBK