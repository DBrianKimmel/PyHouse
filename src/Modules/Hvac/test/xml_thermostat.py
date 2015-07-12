"""
@name:      PyHouse/src/Modules/Hvac/test/xml_thermostat.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 7, 2014
@Summary:

"""


THERMOSTAT_XML = """
        <ThermostatSection>
            <Thermostat Name='Test Thermostat One' Active='True' Key='0'>
                <DeviceFamily>Insteon</DeviceFamily>
                <CoolSetPoint>78.0</CoolSetPoint>
                <CurrentTemperature>76</CurrentTemperature>
                <HeatSetPoint>71.0</HeatSetPoint>
                <ThermostatMode>Cool</ThermostatMode>
                <ThermostatScale>F</ThermostatScale>
                <Address>18.C9.4A</Address>
            </Thermostat>
        </ThermostatSection>
"""
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
