"""
@name:      PyHouse/src/Modules/Lighting/test/xml_buttons.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 22, 2014
@Summary:

"""

__updated__ = '2016-10-05'

# Import system type stuff

# Import PyMh files
from Modules.Core.test.xml_device import XML_DEVICE_INSTEON
from Modules.Families.Insteon.test.xml_insteon import XML_INSTEON_2
from Modules.Families.UPB.test.xml_upb import XML_UPB


L_BUTTON_SECTION_START = '<ButtonSection>'
L_BUTTON_SECTION_END = '</ButtonSection>'
L_BUTTON_END = '</Button>'

TESTING_LIGHTING_BUTTON_TYPE = 'Button'
TESTING_LIGHTING_BUTTON_NAME_0 = 'Insteon Button'
TESTING_LIGHTING_BUTTON_NAME_1 = 'UPB Button'

L_BUTTON_TYPE = '    <LightingType>' + TESTING_LIGHTING_BUTTON_TYPE + '</LightingType>'

L_BUTTON_BODY = '\n'.join([
    XML_DEVICE_INSTEON,
    L_BUTTON_TYPE
    ])

INSTEON_BUTTON_XML = '\n'.join([
    '<Button Name="' + TESTING_LIGHTING_BUTTON_NAME_0 + '" Active="True" Key="0">',
    L_BUTTON_BODY,
    XML_INSTEON_2,
    L_BUTTON_END
    ])

UPB_BUTTON_XML = '\n'.join([
    '<Button Name="' + TESTING_LIGHTING_BUTTON_NAME_1 + '" Active="True" Key="1">',
    L_BUTTON_BODY,
    XML_UPB,
    L_BUTTON_END
    ])

XML_BUTTON_SECTION = '\n'.join([
    L_BUTTON_SECTION_START,
    INSTEON_BUTTON_XML,
    UPB_BUTTON_XML,
    L_BUTTON_SECTION_END
    ])



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
