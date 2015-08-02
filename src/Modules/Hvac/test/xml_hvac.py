"""
@name:      PyHouse/src/Modules/Hvac/xml_hvac.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 1, 2015
@Summary:

"""

# Import system type stuff

# Import PyMh files
from Modules.Core.test.xml_device import XML_DEVICE
from Modules.Families.Insteon.test.xml_insteon import XML_INSTEON


TESTING_THERMOSTAT_NAME = 'Test Thermostat One'
TESTING_THERMOSTAT_ACTIVE = 'True'
TESTING_THERMOSTAT_KEY = '0'


L_THERMOSTAT_NAME = '  <Thermostat Name="' + TESTING_THERMOSTAT_NAME + \
                    '" Active="' + TESTING_THERMOSTAT_ACTIVE + \
                    '" Key="' + TESTING_THERMOSTAT_KEY + '">'

TESTING_THERMOSTAT_COOL_SETPOINT = '78.0'
TESTING_THERMOSTAT_HEAT_SETPOINT = '70.0'
TESTING_THERMOSTAT_SCALE = 'F'
TESTING_THERMOSTAT_MODE = 'Cool'
L_THERMOSTAT_COOL_SETPOINT = '    <CoolSetPoint>' + TESTING_THERMOSTAT_COOL_SETPOINT + '</CoolSetPoint>'
L_THERMOSTAT_HEAT_SETPOINT = '    <HeatSetPoint>' + TESTING_THERMOSTAT_HEAT_SETPOINT + '</HeatSetPoint>'
L_THERMOSTAT_MODE = '    <ThermostatMode>' + TESTING_THERMOSTAT_MODE + '</ThermostatMode>'
L_THERMOSTAT_SCALE = '    <ThermostatScale>' + TESTING_THERMOSTAT_SCALE + '</ThermostatScale>'

TESTING_THERMOSTAT_CURRENT_TEMP = '75.0'
L_THERMOSTAT_CURRENT_TEMP = '    <CurrentTemperature>' + TESTING_THERMOSTAT_CURRENT_TEMP + '</CurrentTemperature>'

L_THERMOSTAT_SETTINGS = '\n'.join([
    L_THERMOSTAT_COOL_SETPOINT,
    L_THERMOSTAT_HEAT_SETPOINT,
    L_THERMOSTAT_MODE,
    L_THERMOSTAT_SCALE
    ])

L_THERMOSTAT_STATUS = '\n'.join([
    L_THERMOSTAT_CURRENT_TEMP
    ])

XML_INSTEON_THERMOSTAT = '\n'.join([
    L_THERMOSTAT_NAME,
    '<!-- ABC -->',
    XML_DEVICE,
    L_THERMOSTAT_SETTINGS,
    L_THERMOSTAT_STATUS,
    XML_INSTEON,
    "</Thermostat>"
    ])

XML_THERMOSTAT = '\n'.join([
        ' <ThermostatSection>',
        '    <!-- A1BC -->',
        XML_INSTEON_THERMOSTAT,
        '    <!-- A1ZY -->',
        ' </ThermostatSection>'
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

# ## END DBK
