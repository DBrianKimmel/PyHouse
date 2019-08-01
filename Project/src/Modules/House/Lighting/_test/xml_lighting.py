"""
@name:      PyHouse/src/Modules/Lighting/_test/xml_lighting.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 17, 2014
@Summary:

See PyHouse/src/_test/xml_data.py for the entire hierarchy.

Config File Version 1.4 placed this entire section under a new LightingSection element.

"""

__updated__ = '2017-01-19'

# Import system type stuff

# Import PyMh files
from Modules.Housing.Lighting.test.xml_buttons import XML_BUTTON_SECTION
from Modules.Housing.Lighting.test.xml_controllers import XML_CONTROLLER_SECTION
from Modules.Housing.Lighting.test.xml_lights import XML_LIGHT_SECTION


TESTING_LIGHTING_SECTION = 'LightingSection'

L_LIGHTING_SECTION_START = '<' + TESTING_LIGHTING_SECTION + '>'
L_LIGHTING_SECTION_END = '</' + TESTING_LIGHTING_SECTION + '>'

XML_LIGHTING = '\n'.join([
    L_LIGHTING_SECTION_START,
    XML_BUTTON_SECTION,
    XML_CONTROLLER_SECTION,
    XML_LIGHT_SECTION,
    L_LIGHTING_SECTION_END
])

# ## END DBK
