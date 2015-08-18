"""
@name:      PyHouse/src/Modules/Lighting/test/xml_lighting.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 17, 2014
@Summary:

See PyHouse/src/test/xml_data.py for the entire hierarchy.

Config File Version 1.4 placed this entire section under a new LightingSection element.

"""

# Import system type stuff

# Import PyMh files
from Modules.Lighting.test.xml_buttons import XML_BUTTON_SECTION
from Modules.Lighting.test.xml_lights import XML_LIGHT_SECTION
from Modules.Lighting.test.xml_controllers import XML_CONTROLLER_SECTION


LIGHTING_XML = '\n'.join([
    '<LightingSection>',
    XML_BUTTON_SECTION,
    XML_LIGHT_SECTION,
    XML_CONTROLLER_SECTION,
    '</LightingSection>'
])

# ## END DBK