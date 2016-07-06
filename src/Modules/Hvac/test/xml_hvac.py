"""
@name:      PyHouse/src/Modules/Hvac/xml_hvac.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 1, 2015
@Summary:

"""

#  Import system type stuff

#  Import PyMh files
from Modules.Core.test.xml_device import XML_DEVICE_INSTEON
from Modules.Families.Insteon.test.xml_insteon import XML_INSTEON

L_HVAC_SECTION_START = '<HvacSection>'
L_HVAC_SECTION_END = '</HvacSection>'
L_THERMOSTAT_SECTION_START = '    <ThermostatSection>'
L_THERMOSTAT_SECTION_END = '      </ThermostatSection>'
L_THERMOSTAT_END = '        </Thermostat>'

TESTING_THERMOSTAT_NAME_0 = 'Test Thermostat Zero'
TESTING_THERMOSTAT_ACTIVE_0 = 'True'
TESTING_THERMOSTAT_KEY_0 = '0'
TESTING_THERMOSTAT_UUID_0 = 'Thermost-0000-0000-0000-0123456789ab'

TESTING_THERMOSTAT_DEVICE_COMMENT_0 = 'Comment zero'
TESTING_THERMOSTAT_DEVICE_FAMILY_0 = 'Insteon'
TESTING_THERMOSTAT_COOL_SETPOINT_0 = '78.0'
TESTING_THERMOSTAT_HEAT_SETPOINT_0 = '70.0'
TESTING_THERMOSTAT_SCALE_0 = 'F'
TESTING_THERMOSTAT_MODE_0 = 'Cool'
TESTING_THERMOSTAT_CURRENT_TEMP_0 = '75.0'

L_THERMOSTAT_START_0 = '          ' + \
        '<Thermostat Name="' + TESTING_THERMOSTAT_NAME_0 + \
        '" Active="' + TESTING_THERMOSTAT_ACTIVE_0 + \
        '" Key="' + TESTING_THERMOSTAT_KEY_0 + '">'
L_THERMOSTAT_UUID_0 = '<UUID>' + TESTING_THERMOSTAT_UUID_0 + '</UUID>'
L_THERMOSTAT_DEVICE_COMMENT_0 = '            <Comment>' + TESTING_THERMOSTAT_DEVICE_COMMENT_0 + '</Comment>'
L_THERMOSTAT_COOL_SETPOINT_0 = '            <CoolSetPoint>' + TESTING_THERMOSTAT_COOL_SETPOINT_0 + '</CoolSetPoint>'
L_THERMOSTAT_HEAT_SETPOINT_0 = '            <HeatSetPoint>' + TESTING_THERMOSTAT_HEAT_SETPOINT_0 + '</HeatSetPoint>'
L_THERMOSTAT_MODE_0 = '            <ThermostatMode>' + TESTING_THERMOSTAT_MODE_0 + '</ThermostatMode>'
L_THERMOSTAT_SCALE_0 = '            <ThermostatScale>' + TESTING_THERMOSTAT_SCALE_0 + '</ThermostatScale>'
L_THERMOSTAT_CURRENT_TEMP_0 = '            <CurrentTemperature>' + TESTING_THERMOSTAT_CURRENT_TEMP_0 + '</CurrentTemperature>'

L_THERMOSTAT_SETTINGS_0 = '\n'.join([
    L_THERMOSTAT_COOL_SETPOINT_0,
    L_THERMOSTAT_HEAT_SETPOINT_0,
    L_THERMOSTAT_MODE_0,
    L_THERMOSTAT_SCALE_0
    ])

L_THERMOSTAT_STATUS_0 = '\n'.join([
    L_THERMOSTAT_CURRENT_TEMP_0
])

XML_INSTEON_THERMOSTAT_0 = '\n'.join([
    L_THERMOSTAT_START_0,
    L_THERMOSTAT_UUID_0,
    XML_DEVICE_INSTEON,
    L_THERMOSTAT_SETTINGS_0,
    L_THERMOSTAT_STATUS_0,
    XML_INSTEON,
    L_THERMOSTAT_END
])


TESTING_THERMOSTAT_NAME_1 = 'Test Thermostat One'
TESTING_THERMOSTAT_ACTIVE_1 = 'True'
TESTING_THERMOSTAT_KEY_1 = '1'
TESTING_THERMOSTAT_UUID_1 = 'Thermost-0001-0001-0001-0123456789ab'
TESTING_THERMOSTAT_DEVICE_FAMILY_1 = 'UPB'

L_THERMOSTAT_START_1 = '     ' + \
        '<Thermostat Name="' + TESTING_THERMOSTAT_NAME_1 + \
        '" Active="' + TESTING_THERMOSTAT_ACTIVE_1 + \
        '" Key="' + TESTING_THERMOSTAT_KEY_1 + \
        '">'
L_THERMOSTAT_UUID_1 = '<UUID>' + TESTING_THERMOSTAT_UUID_1 + '</UUID>'
L_THERMOSTAT_COOL_SETPOINT_1 = '            <CoolSetPoint>' + TESTING_THERMOSTAT_COOL_SETPOINT_0 + '</CoolSetPoint>'
L_THERMOSTAT_HEAT_SETPOINT_1 = '            <HeatSetPoint>' + TESTING_THERMOSTAT_HEAT_SETPOINT_0 + '</HeatSetPoint>'
L_THERMOSTAT_MODE_1 = '            <ThermostatMode>' + TESTING_THERMOSTAT_MODE_0 + '</ThermostatMode>'
L_THERMOSTAT_SCALE_1 = '            <ThermostatScale>' + TESTING_THERMOSTAT_SCALE_0 + '</ThermostatScale>'
L_THERMOSTAT_CURRENT_TEMP_1 = '            <CurrentTemperature>' + TESTING_THERMOSTAT_CURRENT_TEMP_0 + '</CurrentTemperature>'

L_THERMOSTAT_STATUS_1 = '\n'.join([
    L_THERMOSTAT_CURRENT_TEMP_1
])

XML_INSTEON_THERMOSTAT_1 = '\n'.join([
    L_THERMOSTAT_START_1,
    L_THERMOSTAT_UUID_1,
    XML_DEVICE_INSTEON,
    L_THERMOSTAT_SETTINGS_0,
    L_THERMOSTAT_STATUS_1,
    XML_INSTEON,
    L_THERMOSTAT_END
])

XML_HVAC = '\n'.join([
    L_HVAC_SECTION_START,
        L_THERMOSTAT_SECTION_START,
                XML_INSTEON_THERMOSTAT_0,
                XML_INSTEON_THERMOSTAT_1,
        L_THERMOSTAT_SECTION_END,
    L_HVAC_SECTION_END
])

THERMOSTAT_XSD = """"
<xs:schema
    attributeFormDefault="unqualified"
    elementFormDefault="qualified"
    xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <xs:element name="ThermostatSection">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="Thermostat">
          <xs:complexType>
            <xs:sequence>
              <xs:element type="xs:string" name="DeviceFamily"/>
              <xs:element type="xs:float" name="CoolSetPoint"/>
              <xs:element type="xs:byte" name="CurrentTemperature"/>
              <xs:element type="xs:float" name="HeatSetPoint"/>
              <xs:element type="xs:string" name="ThermostatMode"/>
              <xs:element type="xs:string" name="ThermostatScale"/>
              <xs:element type="xs:string" name="Address"/>
            </xs:sequence>
            <xs:attribute type="xs:string" name="Name"/>
            <xs:attribute type="xs:string" name="Active"/>
            <xs:attribute type="xs:byte" name="Key"/>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>

</xs:schema>"""

#  ## END DBK
