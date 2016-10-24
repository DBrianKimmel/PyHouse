"""
@name:      PyHouse/src/Modules/Lighting/test/xml_lighting.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 17, 2014
@Summary:

See PyHouse/src/test/xml_data.py for the entire hierarchy.

Config File Version 1.4 placed this entire section under a new LightingSection element.

"""

__updated__ = '2016-10-22'

# Import system type stuff

# Import PyMh files
from Modules.Housing.Lighting.test.xml_buttons import XML_BUTTON_SECTION
from Modules.Housing.Lighting.test.xml_controllers import XML_CONTROLLER_SECTION
from Modules.Housing.Lighting.test.xml_garagedoors import XML_GARAGE_DOOR_SECTION
from Modules.Housing.Lighting.test.xml_lights import XML_LIGHT_SECTION
from Modules.Housing.Lighting.test.xml_motion import XML_LIGHTING_MOTION_SECTION


L_LIGHTING_SECTION_START = '<LightingSection>'
L_LIGHTING_SECTION_END = '</LightingSection>'

XML_LIGHTING = '\n'.join([
    L_LIGHTING_SECTION_START,
    XML_BUTTON_SECTION,
    XML_CONTROLLER_SECTION,
    XML_LIGHT_SECTION,
    XML_GARAGE_DOOR_SECTION,
    XML_LIGHTING_MOTION_SECTION,
    L_LIGHTING_SECTION_END
])

# ## END DBK
