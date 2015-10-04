"""
@name:      PyHouse/src/Modules/Irrigation/test/xml_irrigation.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c)  2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 30, 2015
@Summary:

"""

TESTING_IRRIGATION_SYSTEM_NAME_0 = 'LawnSystem'
TESTING_IRRIGATION_SYSTEM_KEY_0 = '0'
TESTING_IRRIGATION_SYSTEM_ACTIVE_0 = 'True'
TESTING_IRRIGATION_SYSTEM_COMMENT_0 = 'Main yard system with Well Relay and 13 zones'

TESTING_IRRIGATION_SYSTEM_NAME_1 = 'Lanai Drip'
TESTING_IRRIGATION_SYSTEM_KEY_1 = '1'
TESTING_IRRIGATION_SYSTEM_ACTIVE_1 = 'True'

L_IRRIGATION_SECTION_START = '<IrrigationSection>'
L_IRRIGATION_SECTION_END = '</IrrigationSection>'

L_IRRIGATION_SYSTEM_START_0 = '<IrrigationSystem Name="' + TESTING_IRRIGATION_SYSTEM_NAME_0 + \
        '" Key="' + TESTING_IRRIGATION_SYSTEM_KEY_0 + \
        '" Active="' + TESTING_IRRIGATION_SYSTEM_ACTIVE_0 + \
        '">'
L_IRRIGATION_SYSTEM_COMMENT_0 = '<Comment>' + TESTING_IRRIGATION_SYSTEM_COMMENT_0 + '</Comment>'

L_IRRIGATION_SYSTEM_START_1 = '<IrrigationSystem Name="' + TESTING_IRRIGATION_SYSTEM_NAME_1 + \
        '" Key="' + TESTING_IRRIGATION_SYSTEM_KEY_1 + \
        '" Active="' + TESTING_IRRIGATION_SYSTEM_ACTIVE_1 + \
        '">'
L_IRRIGATION_SYSTEM_END = '</IrrigationSystem>'

XXX_0 = """
        <Comment>Main yard system with Well Relay and 13 zones</Comment>
        <Zone Name="Front Rotors # 1" Key="0" Active="True">
            <Comment>Rotors on the West corner of the yard,</Comment>
            <Duration>2700</Duration>
        </Zone>
        <Zone Name="Front Rotors # 2" Key="1" Active="True">
            <Comment>Rotors on the driveway side of the yard,</Comment>
            <Duration>2700</Duration>
        </Zone>
        <Zone Name="Front Rotors # 3" Key="2" Active="True">
        </Zone>
        <Zone Name="Front Rotors # 4" Key="3" Active="True">
        </Zone>
        <Zone Name="Front Rotors # 5" Key="4" Active="True">
        </Zone>
        <Zone Name="Front Rotors # 6" Key="5" Active="True">
        </Zone>
        <Zone Name="Front Rotors # 7" Key="6" Active="True">
        </Zone>
"""
XXX_1 = """
        <Comment>Lanai area system</Comment>
        <Zone Name="Flower Drips" Key="0" Active="True">
        </Zone>
        <Zone Name="Pool Filler" Key="1" Active="True">
        </Zone>
        <Zone Name="UnUsed" Key="2" Active="True">
        </Zone>
"""

L_IRRIGATION_SYSTEM_0 = '\n'.join([
    L_IRRIGATION_SYSTEM_START_0,
        L_IRRIGATION_SYSTEM_COMMENT_0,
        XXX_0,
    L_IRRIGATION_SYSTEM_END
])

L_IRRIGATION_SYSTEM_1 = '\n'.join([
    L_IRRIGATION_SYSTEM_START_1,
        XXX_1,
    L_IRRIGATION_SYSTEM_END
])

XML_IRRIGATION = '\n'.join([
    L_IRRIGATION_SECTION_START,
        L_IRRIGATION_SYSTEM_0,
        L_IRRIGATION_SYSTEM_1,
    L_IRRIGATION_SECTION_END
])



IRRIGATION_XSD = """
<xs:schema
    attributeFormDefault="unqualified"
    elementFormDefault="qualified"
    xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <xs:element name="IrrigationSection">
  </xs:element>

</xs:schema>
"""
# ## END DBK
