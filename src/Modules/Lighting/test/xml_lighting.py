"""
@name:      PyHouse/src/Modules/Lighting/test/xml_lighting.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 17, 2014
@Summary:

Config File Version 1.4 placed this entire section under a new LightingSection element.

"""

# Import system type stuff

# Import PyMh files
from Modules.Lighting.test.xml_buttons import BUTTON_SECTION_XML
from Modules.Lighting.test.xml_lights import *
from Modules.Lighting.test.xml_controllers import *



LIGHTING_XML = '\n'.join([
    '<LightingSection>',
    BUTTON_SECTION_XML,
    LIGHT_SECTION_XML,
    CONTROLLER_SECTION_XML,
    '</LightingSection>'
])

# ## END DBK