"""
@name:      PyHouse/src/Modules/Lighting/test/xml_buttons.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 22, 2014
@Summary:

2 *
"""

# Import system type stuff

# Import PyMh files
from Modules.Lighting.test.xml_core import *
from Modules.Families.Insteon.test.xml_insteon import *
from Modules.Families.UPB.test.xml_upb import *



BUTTON_TYPE = "    <LightingType>Button</LightingType>"

BUTTON_BODY = '\n'.join([
    CORE_DEVICE,
    BUTTON_TYPE
    ])

INSTEON_BUTTON_XML = '\n'.join([
    '<Button Active="True" Key="0" Name="Insteon Button">',
    BUTTON_BODY,
    INSTEON_XML,
    "</Button>"])

UPB_BUTTON_XML = '\n'.join([
    '<Button Active="True" Key="1" Name="UPB Button">',
    BUTTON_BODY,
    UPB_XML,
    "</Button>"])

BUTTON_SECTION_XML = '\n'.join([
    "<ButtonSection>",
    INSTEON_BUTTON_XML,
    UPB_BUTTON_XML,
    "</ButtonSection>"])



BUTTON_SECTION_XSD = """
<xs:schema
    attributeFormDefault="unqualified"
    elementFormDefault="qualified"
    xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <xs:element name="ControllerSection">
  </xs:element>
</xs:schema>
"""

# ## END DBK
