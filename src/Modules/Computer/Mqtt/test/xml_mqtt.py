"""
@name:      PyHouse/src/Modules/Computer/Mqtt/test/xml_mqtt.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2015
@Summary:

"""

__updated__ = '2016-07-06'

#  Import system type stuff

#  Import PyMh files


L_MQTT_SECTION_START = '  <MqttSection>'
L_MQTT_SECTION_END = '  </MqttSection>'
L_MQTT_BROKER_END = '    </Broker>'

TESTING_BROKER_NAME_0 = 'CannonTrail'
TESTING_BROKER_KEY_0 = '0'
TESTING_BROKER_ACTIVE_0 = 'True'
TESTING_BROKER_UUID_0 = 'Broker..-0000-0000-0000-0123456789ab'
TESTING_BROKER_ADDRESS_0 = '192.168.1.2'
TESTING_BROKER_PORT_0 = '1883'
TESTING_BROKER_USERNAME_0 = 'pyhouse'
TESTING_BROKER_PASSWORD_0 = 'ChangeMe'

L_BROKER_START_0 = '    ' + \
    '<Broker Name="' + TESTING_BROKER_NAME_0 + \
    '" Key="' + TESTING_BROKER_KEY_0 + \
    '" Active="' + TESTING_BROKER_ACTIVE_0 + \
    '">'
L_BROKER_UUID_0 = '      <UUID>' + TESTING_BROKER_UUID_0 + '</UUID>'
L_BROKER_ADDRESS_0 = '      <BrokerAddress>' + TESTING_BROKER_ADDRESS_0 + '</BrokerAddress>'
L_BROKER_PORT_0 = '      <BrokerPort>' + TESTING_BROKER_PORT_0 + '</BrokerPort>'
L_BROKER_USER_0 = '      <BrokerUser>' + TESTING_BROKER_USERNAME_0 + '</BrokerUser>'
L_BROKER_PASSWORD_0 = '      <BrokerPassword>' + TESTING_BROKER_PASSWORD_0 + '</BrokerPassword>'

L_BROKER_0 = '\n'.join([
    L_BROKER_START_0,
    L_BROKER_UUID_0,
    L_BROKER_ADDRESS_0,
    L_BROKER_PORT_0,
    L_BROKER_USER_0,
    L_BROKER_PASSWORD_0,
    L_MQTT_BROKER_END
])

TESTING_BROKER_NAME_1 = 'PinkPoppy'
TESTING_BROKER_KEY_1 = '1'
TESTING_BROKER_ACTIVE_1 = 'True'
TESTING_BROKER_UUID_1 = 'Broker..-0001-0001-0001-0123456789ab'
TESTING_BROKER_ADDRESS_1 = '192.168.1.3'
TESTING_BROKER_PORT_1 = '8883'
TESTING_BROKER_USERNAME_1 = 'pyhouse'
TESTING_BROKER_PASSWORD_1 = 'ChangeMe'

L_BROKER_START_1 = '    ' + \
    '<Broker Name="' + TESTING_BROKER_NAME_1 + \
    '" Key="' + TESTING_BROKER_KEY_1 + \
    '" Active="' + TESTING_BROKER_ACTIVE_1 + \
    '">'
L_BROKER_UUID_1 = '      <UUID>' + TESTING_BROKER_UUID_1 + '</UUID>'
L_BROKER_ADDRESS_1 = '      <BrokerAddress>' + TESTING_BROKER_ADDRESS_1 + '</BrokerAddress>'
L_BROKER_PORT_1 = '      <BrokerPort>' + TESTING_BROKER_PORT_1 + '</BrokerPort>'
L_BROKER_USER_1 = '      <BrokerUser>' + TESTING_BROKER_USERNAME_1 + '</BrokerUser>'
L_BROKER_PASSWORD_1 = '      <BrokerPassword>' + TESTING_BROKER_PASSWORD_1 + '</BrokerPassword>'

L_BROKER_1 = '\n'.join([
    L_BROKER_START_1,
    L_BROKER_UUID_1,
    L_BROKER_ADDRESS_1,
    L_BROKER_PORT_1,
    L_BROKER_USER_1,
    L_BROKER_PASSWORD_1,
    L_MQTT_BROKER_END
])

XML_MQTT = '\n'.join([
    L_MQTT_SECTION_START,
    L_BROKER_0,
    L_BROKER_1,
    L_MQTT_SECTION_END
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

#  ## END DBK
