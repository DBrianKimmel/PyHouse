"""
@name:      PyHouse/src/Modules/Hvac/test/xml_thermostat.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 7, 2014
@Summary:

"""

TESTING_THERMOSTAT_NAME_0 = 'Test Thermostat One'
TESTING_THERMOSTAT_ACTIVE_0 = 'True'
TESTING_THERMOSTAT_KEY_0 = '0'
TESTING_THERMOSTAT_DEVICE_FAMILY_0 = 'Insteon'
TESTING_THERMOSTAT_COOL_SETPOINT_0 = '78.0'
TESTING_THERMOSTAT_HEAT_SETPOINT_0 = '70.0'
TESTING_THERMOSTAT_SCALE_0 = 'F'
TESTING_THERMOSTAT_MODE_0 = 'Cool'
TESTING_THERMOSTAT_ADDRESS = '18.C9.4A'
TESTING_THERMOSTAT_CURRENT_TEMP_0 = '75.0'

L_THERMOSTAT_BASE = '  <Thermostat Name="' + TESTING_THERMOSTAT_NAME_0 + \
                    '" Active="' + TESTING_THERMOSTAT_ACTIVE_0 + \
                    '" Key="' + TESTING_THERMOSTAT_KEY_0 + '">'
L_THERMOSTAT_DEVICE_FAMILY = '    <DeviceFamily>' + TESTING_THERMOSTAT_DEVICE_FAMILY_0 + '</DeviceFamily>'
L_THERMOSTAT_COOL_SETPOINT = '    <CoolSetPoint>' + TESTING_THERMOSTAT_COOL_SETPOINT_0 + '</CoolSetPoint>'
L_THERMOSTAT_HEAT_SETPOINT = '    <HeatSetPoint>' + TESTING_THERMOSTAT_HEAT_SETPOINT_0 + '</HeatSetPoint>'
L_THERMOSTAT_MODE = '    <ThermostatMode>' + TESTING_THERMOSTAT_MODE_0 + '</ThermostatMode>'
L_THERMOSTAT_SCALE = '    <ThermostatScale>' + TESTING_THERMOSTAT_SCALE_0 + '</ThermostatScale>'
L_THERMOSTAT_ADDRESS = '    <Address>' + TESTING_THERMOSTAT_ADDRESS + '</Address>'
L_THERMOSTAT_CURRENT_TEMP = '    <CurrentTemperature>' + TESTING_THERMOSTAT_CURRENT_TEMP_0 + '</CurrentTemperature>'


XML_THERMOSTAT_XX = '\n'.join([
        '<ThermostatSection>',
        L_THERMOSTAT_BASE,
        L_THERMOSTAT_DEVICE_FAMILY,
        L_THERMOSTAT_COOL_SETPOINT,
        L_THERMOSTAT_HEAT_SETPOINT,
        L_THERMOSTAT_MODE,
        L_THERMOSTAT_SCALE,
        L_THERMOSTAT_ADDRESS,
        L_THERMOSTAT_CURRENT_TEMP,
        '  </Thermostat>',
        '</ThermostatSection>'
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
