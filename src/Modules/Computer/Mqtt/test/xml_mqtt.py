"""
@name:      PyHouse/src/Modules/Computer/Mqtt/test/xml_mqtt.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2015
@Summary:

"""
# from Modules.Computer.Mqtt.test.xml_mqtt import TESTING_BROKER_NAME_1

# Import system type stuff

# Import PyMh files

TESTING_BROKER_NAME_1 = 'iot.eclipse'
TESTING_BROKER_KEY_1 = '0'
TESTING_BROKER_ACTIVE_1 = 'False'
TESTING_BROKER_ADDRESS_1 = '2001:db8::dead.beef'
TESTING_BROKER_PORT_1 = '1883'
TESTING_BROKER_NAME_2 = 'PinkPoppy'
TESTING_BROKER_KEY_2 = '1'
TESTING_BROKER_ACTIVE_2 = 'True'
TESTING_BROKER_ADDRESS_2 = '192.168.1.2'
TESTING_BROKER_PORT_2 = '1883'

L_BROKER_MAIN_1 = '    <Broker Name="' + TESTING_BROKER_NAME_1 + '" Key="' + TESTING_BROKER_KEY_1 + '" Active="' + TESTING_BROKER_ACTIVE_1 + '">'
L_BROKER_MAIN_2 = '    <Broker Name="' + TESTING_BROKER_NAME_2 + '" Key="' + TESTING_BROKER_KEY_2 + '" Active="' + TESTING_BROKER_ACTIVE_2 + '">'
L_BROKER_ADDRESS_1 = '      <BrokerAddress>' + TESTING_BROKER_ADDRESS_1 + '</BrokerAddress>'
L_BROKER_ADDRESS_2 = '      <BrokerAddress>' + TESTING_BROKER_ADDRESS_2 + '</BrokerAddress>'
L_BROKER_PORT_1 = '      <BrokerPort>' + TESTING_BROKER_PORT_1 + '</BrokerPort>'
L_BROKER_PORT_2 = '      <BrokerPort>' + TESTING_BROKER_PORT_2 + '</BrokerPort>'

XML_MQTT = '\n'.join([
    '  <MqttSection>',
    L_BROKER_MAIN_1,
    L_BROKER_ADDRESS_1,
    L_BROKER_PORT_1,
    '  </Broker>',
    L_BROKER_MAIN_2,
    L_BROKER_ADDRESS_2,
    L_BROKER_PORT_2,
    '  </Broker>',
    '  </MqttSection>'
    ])

MQTT_XSD = """
<xs:schema
    attributeFormDefault="unqualified"
    elementFormDefault="qualified"
    xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <xs:element name="MqttSection">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="Broker" maxOccurs="unbounded" Occurs="1">
          <xs:complexType>
            <xs:sequence>
              <xs:element type="xs:string" name="BrokerAddress"/>
              <xs:element type="xs:string" name="BrokerPort"/>
            </xs:sequence>
            <xs:attribute type="xs:string" name="Name" use="optional"/>
            <xs:attribute type="xs:byte" name="Key" use="optional"/>
            <xs:attribute type="xs:string" name="Active" use="optional"/>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
"""

# ## END DBK
