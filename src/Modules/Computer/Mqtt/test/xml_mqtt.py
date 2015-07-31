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

TESTING_BROKER_NAME_1 = 'iot.eclipse.org'
TESTING_BROKER_ADDRESS_1 = '1234:5678::dead.beef'
TESTING_BROKER_PORT_1 = '1833'
TESTING_BROKER_NAME_2 = 'PinkPoppy.pyhouse.org'
TESTING_BROKER_ADDRESS_2 = '192.168.1.51'
TESTING_BROKER_PORT_2 = '1833'


XML_MQTT = """\
    <MqttSection>
        <Broker Name='""" + TESTING_BROKER_NAME_1 + """' Key='0' Active='True'>
            <BrokerAddress>""" + TESTING_BROKER_ADDRESS_1 + """</BrokerAddress>
            <BrokerPort>""" + TESTING_BROKER_PORT_1 + """</BrokerPort>
        </Broker>
        <Broker Name='""" + TESTING_BROKER_NAME_2 + """' Key='1' Active='True'>
            <BrokerAddress>""" + TESTING_BROKER_ADDRESS_2 + """</BrokerAddress>
            <BrokerPort>""" + TESTING_BROKER_PORT_2 + """</BrokerPort>
        </Broker>
    </MqttSection>
"""



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
