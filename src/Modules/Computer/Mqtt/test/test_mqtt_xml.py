"""
@name:      PyHouse/src/Modules/Computer/Mqtt/test/test_mqtt_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 4, 2015  --updated
@Summary:   Test the read and write of MQTT sections of XML

Passed all 11 tests - DBK - 2017-01-11

"""

__updated__ = '2017-01-20'

#  Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

#  Import PyMh files and modules.
from Modules.Computer.Mqtt.mqtt_xml import Xml as mqttXML
from test.xml_data import XML_LONG, XML_EMPTY, TESTING_PYHOUSE
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
    TESTING_BROKER_PASSWORD_1, TESTING_BROKER_UUID_0, XML_MQTT, TESTING_MQTT_SECTION
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = mqttXML()


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_mqtt_xml')


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')
        self.assertEqual(self.m_xml.mqtt_sect.tag, 'MqttSection')
        self.assertEqual(self.m_xml.broker.tag, 'Broker')

    def test_02_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml.mqtt_sect, 'A1-02-A - Tags'))

    def test_03_Mqtt(self):
        pass


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_MQTT
        print(l_raw)
        self.assertEqual(l_raw[:13], '<MqttSection>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_MQTT)
        # print(l_xml)
        self.assertEqual(l_xml.tag, TESTING_MQTT_SECTION)


class B1_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Broker(self):
        """ Read one broker
        """
        l_obj = mqttXML._read_one_broker(self.m_xml.broker)
        # print(PrettyFormatAny.form(l_obj, 'B1-01-A - Broker'))
        self.assertEqual(l_obj.Name, TESTING_BROKER_NAME_0)
        self.assertEqual(l_obj.Key, int(TESTING_BROKER_KEY_0))
        self.assertEqual(str(l_obj.Active), TESTING_BROKER_ACTIVE_0)
        self.assertEqual(l_obj.UUID, TESTING_BROKER_UUID_0)
        self.assertEqual(l_obj.BrokerAddress, TESTING_BROKER_ADDRESS_0)
        self.assertEqual(l_obj.BrokerPort, int(TESTING_BROKER_PORT_0))
        self.assertEqual(l_obj.UserName, TESTING_BROKER_USERNAME_0)
        self.assertEqual(l_obj.Password, TESTING_BROKER_PASSWORD_0)

    def test_02_Mqtt(self):
        """Here we should get a dict of brokers
        """
        l_obj = self.m_api.read_mqtt_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'B1-02-A - Broker'))
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


class B2_EmptyRead(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_EMPTY))

    def test_01_Mqtt(self):
        """Here we should get a dict of brokers
        """
        l_obj = self.m_api.read_mqtt_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'Mqtt'))
        self.assertEqual(l_obj, {})


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
        # print(PrettyFormatAny.form(l_xml, 'C1-01-A - Broker'))
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
