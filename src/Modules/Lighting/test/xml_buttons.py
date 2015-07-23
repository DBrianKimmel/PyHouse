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
from Modules.Core.test.xml_device import XML_DEVICE
from Modules.Families.Insteon.test.xml_insteon import XML_INSTEON
from Modules.Families.UPB.test.xml_upb import UPB_XML



L_BUTTON_TYPE = "    <LightingType>Button</LightingType>"

L_BUTTON_BODY = '\n'.join([
    XML_DEVICE,
    L_BUTTON_TYPE
    ])

INSTEON_BUTTON_XML = '\n'.join([
    '<Button Active="True" Key="0" Name="Insteon Button">',
    L_BUTTON_BODY,
    XML_INSTEON,
    "</Button>"])

UPB_BUTTON_XML = '\n'.join([
    '<Button Active="True" Key="1" Name="UPB Button">',
    L_BUTTON_BODY,
    UPB_XML,
    "</Button>"])

XML_BUTTON_SECTION = '\n'.join([
    "<ButtonSection>",
    INSTEON_BUTTON_XML,
    UPB_BUTTON_XML,
    "</ButtonSection>"])



XSD_BUTTON_SECTION = """
<xs:schema
    attributeFormDefault="unqualified"
    elementFormDefault="qualified"
    xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <xs:element name="ControllerSection">
  </xs:element>
</xs:schema>
"""

# ## END DBK
