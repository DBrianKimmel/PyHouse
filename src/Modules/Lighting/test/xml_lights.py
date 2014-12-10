"""
@name: C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/Lighting/test/xml_lights.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Nov 22, 2014
@Summary:

"""

# Import system type stuff

# Import PyMh files
from Modules.Lighting.test.xml_core import *
from Modules.Families.Insteon.test.xml_insteon import INSTEON_XML
from Modules.Families.UPB.test.xml_upb import UPB_XML


TESTING_LIGHTING_LIGHT_CUR_LEVEL = "12"


LIGHT_TYPE = "    <LightingType>Light</LightingType>"

LIGHT_BODY = '\n'.join([
    CORE_DEVICE,
    LIGHT_TYPE,
    "<CurLevel>" + TESTING_LIGHTING_LIGHT_CUR_LEVEL + "</CurLevel>"
    ])

INSTEON_LIGHT_XML = '\n'.join([
    '<Light Active="True" Key="0" Name="Insteon Light">',
    LIGHT_BODY,
    INSTEON_XML,
    "</Light>"])

UPB_LIGHT_XML = '\n'.join([
    '<Light Active="True" Key="1" Name="UPB Light">',
    LIGHT_BODY,
    UPB_XML,
    "</Light>"])

LIGHT_SECTION_XML = '\n'.join([
    "<LightSection>",
    INSTEON_LIGHT_XML,
    UPB_LIGHT_XML,
    "</LightSection>"])

# ## END DBK
