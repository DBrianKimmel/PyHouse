"""
@name:      PyHouse/src/Modules/Computer/Mqtt/test/test_mqtt_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 4, 2015
@Summary:   Test the read and write of MQTT sections of XML

Passed all 7 tests - DBK - 2016-01-22

"""

#  Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

#  Import PyMh files and modules.
from Modules.Computer.Mqtt.mqtt_xml import Xml as mqttXML
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Computer.Mqtt.test.xml_mqtt import \
    TESTING_BROKER_NAME_0, \
    TESTING_BROKER_KEY_0, \
    TESTING_BROKER_ACTIVE_0, \
    TESTING_BROKER_ADDRESS_0, \
    TESTING_BROKER_PORT_0, \
    TESTING_BROKER_NAME_1, \
    TESTING_BROKER_KEY_1, \
    TESTING_BROKER_ACTIVE_1, \
    TESTING_BROKER_ADDRESS_1, \
    TESTING_BROKER_PORT_1, \
    TESTING_BROKER_USERNAME_0, \
    TESTING_BROKER_PASSWORD_0, \
    TESTING_BROKER_USERNAME_1, \
    TESTING_BROKER_PASSWORD_1
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = mqttXML()


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        """ Be sure that the XML contains the right stuff.
        """
        pass

    def test_02_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')
        self.assertEqual(self.m_xml.mqtt_sect.tag, 'MqttSection')

    def test_03_Mqtt(self):
        pass


class B1_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Broker(self):
        """ Read one broker
        """
        l_obj = mqttXML._read_one_broker(self.m_xml.broker)
        #  print(PrettyFormatAny.form(l_obj, 'Broker'))
        self.assertEqual(l_obj.Name, TESTING_BROKER_NAME_0)
        self.assertEqual(l_obj.Key, int(TESTING_BROKER_KEY_0))
        self.assertEqual(l_obj.Active, bool(TESTING_BROKER_ACTIVE_0 == 'True'))
        self.assertEqual(l_obj.BrokerAddress, TESTING_BROKER_ADDRESS_0)
        self.assertEqual(l_obj.BrokerPort, int(TESTING_BROKER_PORT_0))
        self.assertEqual(l_obj.UserName, TESTING_BROKER_USERNAME_0)
        self.assertEqual(l_obj.Password, TESTING_BROKER_PASSWORD_0)

    def test_02_Mqtt(self):
        """Here we should get a dict of brokers
        """
        l_obj = self.m_api.read_mqtt_xml(self.m_pyhouse_obj)
        self.assertEqual(l_obj[0].Name, TESTING_BROKER_NAME_0)
        self.assertEqual(l_obj[0].Key, int(TESTING_BROKER_KEY_0))
        self.assertEqual(l_obj[0].Active, bool(TESTING_BROKER_ACTIVE_0 == 'True'))
        self.assertEqual(l_obj[0].BrokerAddress, TESTING_BROKER_ADDRESS_0)
        self.assertEqual(l_obj[0].BrokerPort, int(TESTING_BROKER_PORT_0))
        self.assertEqual(l_obj[1].Name, TESTING_BROKER_NAME_1)
        self.assertEqual(l_obj[1].Key, int(TESTING_BROKER_KEY_1))
        self.assertEqual(l_obj[1].Active, bool(TESTING_BROKER_ACTIVE_1 == 'True'))
        self.assertEqual(l_obj[1].BrokerAddress, TESTING_BROKER_ADDRESS_1)
        self.assertEqual(l_obj[1].BrokerPort, int(TESTING_BROKER_PORT_1))
        self.assertEqual(l_obj[1].UserName, TESTING_BROKER_USERNAME_1)
        self.assertEqual(l_obj[1].Password, TESTING_BROKER_PASSWORD_1)


class C1_Write(SetupMixin, unittest.TestCase):
    """
    Test writing out XML pieces of Mqtt info
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Broker(self):
        """Write one broker
        """
        l_mqtt_obj = self.m_api.read_mqtt_xml(self.m_pyhouse_obj)[0]
        l_xml = mqttXML._write_one_broker(l_mqtt_obj)
        self.assertEqual(l_mqtt_obj.BrokerAddress, TESTING_BROKER_ADDRESS_0)
        self.assertEqual(l_xml.attrib['Name'], TESTING_BROKER_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_BROKER_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_BROKER_ACTIVE_0)
        self.assertEqual(l_xml.find('BrokerAddress').text, TESTING_BROKER_ADDRESS_0)
        self.assertEqual(l_xml.find('BrokerPort').text, TESTING_BROKER_PORT_0)
        self.assertEqual(l_xml.find('BrokerUser').text, TESTING_BROKER_USERNAME_0)
        self.assertEqual(l_xml.find('BrokerPassword').text, TESTING_BROKER_PASSWORD_0)

    def test_02_Mqtt(self):
        """Write entire Mqtt XML section
        """
        l_mqtt_obj = self.m_api.read_mqtt_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_mqtt_xml(l_mqtt_obj)
        l_xml1 = l_xml.find('Broker')
        #  print(PrettyFormatAny.form(l_xml, 'XML'))
        self.assertEqual(l_xml1.attrib['Name'], TESTING_BROKER_NAME_0)
        self.assertEqual(l_xml1.attrib['Key'], TESTING_BROKER_KEY_0)
        self.assertEqual(l_xml1.attrib['Active'], TESTING_BROKER_ACTIVE_0)
        self.assertEqual(l_xml1.find('BrokerAddress').text, TESTING_BROKER_ADDRESS_0)
        self.assertEqual(l_xml1.find('BrokerPort').text, TESTING_BROKER_PORT_0)
        self.assertEqual(l_xml1.find('BrokerUser').text, TESTING_BROKER_USERNAME_0)
        self.assertEqual(l_xml1.find('BrokerPassword').text, TESTING_BROKER_PASSWORD_0)
        #
        l_xml2 = l_xml[1]
        self.assertEqual(l_xml2.attrib['Name'], TESTING_BROKER_NAME_1)
        self.assertEqual(l_xml2.attrib['Key'], TESTING_BROKER_KEY_1)
        self.assertEqual(l_xml2.attrib['Active'], TESTING_BROKER_ACTIVE_1)
        self.assertEqual(l_xml2.find('BrokerAddress').text, TESTING_BROKER_ADDRESS_1)
        self.assertEqual(l_xml2.find('BrokerPort').text, TESTING_BROKER_PORT_1)
        self.assertEqual(l_xml2.find('BrokerUser').text, TESTING_BROKER_USERNAME_1)
        self.assertEqual(l_xml2.find('BrokerPassword').text, TESTING_BROKER_PASSWORD_1)

#  ## END DBK
