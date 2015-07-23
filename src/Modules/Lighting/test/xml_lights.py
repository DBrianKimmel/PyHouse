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
from Modules.Families.UPB.test.xml_upb import UPB_XML
from Modules.Core.test.xml_device import XML_DEVICE


TESTING_LIGHTING_LIGHTS_INSTEON_NAME = "Insteon Light"
TESTING_LIGHT_DIMMABLE = 'True'
TESTING_LIGHTING_LIGHT_CUR_LEVEL = "12"
TESTING_LIGHTING_TYPE = 'Light'

L_LIGHT_TYPE = '    <LightingType>' + TESTING_LIGHTING_TYPE + '</LightingType>'
L_DIMMABLE = '    <IsDimmable>' + TESTING_LIGHT_DIMMABLE + '</IsDimmable>'
L_LEVEL = "    <CurLevel>" + TESTING_LIGHTING_LIGHT_CUR_LEVEL + "</CurLevel>"

L_LIGHT_BODY = '\n'.join([
    XML_DEVICE,
    L_LIGHT_TYPE,
    L_DIMMABLE,
    L_LEVEL
    ])

L_INSTEON_LIGHT_XML = '\n'.join([
    '<Light Name="' + TESTING_LIGHTING_LIGHTS_INSTEON_NAME + '" Key="0" Active="True">',
    L_LIGHT_BODY,
    XML_INSTEON,
    "</Light>"
    ])

L_UPB_LIGHT_XML = '\n'.join([
    '<Light Name="UPB Light" Key="1" Active="True">',
    L_LIGHT_BODY,
    UPB_XML,
    "</Light>"
    ])

XML_LIGHT_SECTION = '\n'.join([
    "<LightSection>",
    L_INSTEON_LIGHT_XML,
    L_UPB_LIGHT_XML,
    "</LightSection>"
    ])

# ## END DBK
