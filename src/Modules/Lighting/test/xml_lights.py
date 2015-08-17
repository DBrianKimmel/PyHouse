"""
@name:      PyHouse/src/Modules/Lighting/test/xml_lights.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 22, 2014
@Summary:

See PyHouse/src/test/xml_data.py for the entire hierarchy.

"""

# Import system type stuff

# Import PyMh files
from Modules.Families.Insteon.test.xml_insteon import XML_INSTEON
from Modules.Families.UPB.test.xml_upb import XML_UPB
from Modules.Core.test.xml_device import XML_DEVICE_INSTEON


TESTING_LIGHTING_LIGHTS_NAME_1 = "Insteon Light"
TESTING_LIGHTING_LIGHTS_KEY_1 = '0'
TESTING_LIGHTING_LIGHTS_ACTIVE_1 = 'True'
TESTING_LIGHTING_LIGHTS_NAME_2 = "UPB Light"
TESTING_LIGHTING_LIGHTS_KEY_2 = '1'
TESTING_LIGHTING_LIGHTS_ACTIVE_2 = 'True'
TESTING_LIGHT_DIMMABLE = 'True'
TESTING_LIGHTING_LIGHT_CUR_LEVEL = "12"
TESTING_LIGHTING_TYPE = 'Light'

L_LIGHT_LIGHT_1 = '<Light Name="' + TESTING_LIGHTING_LIGHTS_NAME_1 + '" Key="' + TESTING_LIGHTING_LIGHTS_KEY_1 + '" Active="' + TESTING_LIGHTING_LIGHTS_ACTIVE_1 + '">'
L_LIGHT_LIGHT_2 = '<Light Name="' + TESTING_LIGHTING_LIGHTS_NAME_2 + '" Key="' + TESTING_LIGHTING_LIGHTS_KEY_2 + '" Active="' + TESTING_LIGHTING_LIGHTS_ACTIVE_2 + '">'
L_LIGHT_TYPE = '    <LightingType>' + TESTING_LIGHTING_TYPE + '</LightingType>'
L_DIMMABLE = '    <IsDimmable>' + TESTING_LIGHT_DIMMABLE + '</IsDimmable>'
L_LEVEL = "    <CurLevel>" + TESTING_LIGHTING_LIGHT_CUR_LEVEL + "</CurLevel>"

L_LIGHT_BODY = '\n'.join([
    XML_DEVICE_INSTEON,
    L_LIGHT_TYPE,
    L_DIMMABLE,
    L_LEVEL
    ])

L_INSTEON_LIGHT_XML = '\n'.join([
    L_LIGHT_LIGHT_1,
    L_LIGHT_BODY,
    XML_INSTEON,
    "</Light>"
    ])

L_UPB_LIGHT_XML = '\n'.join([
    L_LIGHT_LIGHT_2,
    L_LIGHT_BODY,
    XML_UPB,
    "</Light>"
    ])

XML_LIGHT_SECTION = '\n'.join([
    "<LightSection>",
    L_INSTEON_LIGHT_XML,
    L_UPB_LIGHT_XML,
    "</LightSection>"
    ])

# ## END DBK
