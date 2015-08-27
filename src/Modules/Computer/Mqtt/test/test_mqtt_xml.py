"""
@name:      PyHouse/src/Modules/Computer/Mqtt/test/test_mqtt_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 4, 2015
@Summary:   Test the read and write of MQTT sections of XML

Passed all 7 tests - DBK - 2015-08-03

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Computer.Mqtt.mqtt_xml import Xml as mqttXML
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Computer.Mqtt.test.xml_mqtt import \
    TESTING_BROKER_NAME_1, \
    TESTING_BROKER_KEY_1, \
    TESTING_BROKER_ACTIVE_1, \
    TESTING_BROKER_ADDRESS_1, \
    TESTING_BROKER_PORT_1, \
    TESTING_BROKER_NAME_2, \
    TESTING_BROKER_KEY_2, \
    TESTING_BROKER_ACTIVE_2, \
    TESTING_BROKER_ADDRESS_2, \
    TESTING_BROKER_PORT_2
from Modules.Utilities.tools import PrettyPrintAny


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
        # PrettyPrintAny(self.m_xml.root, 'XML')
        # PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse_obj')
        pass

    def test_02_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        # PrettyPrintAny(self.m_pyhouse_obj.Xml, 'PyHouse XML')
        # PrettyPrintAny(self.m_xml.root, 'XML')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')
        self.assertEqual(self.m_xml.mqtt_sect.tag, 'MqttSection')

    def test_03_Mqtt(self):
        # PrettyPrintAny(self.m_xml.mqtt_sect, 'Mqtt')
        pass


class B1_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Broker(self):
        """ Read one broker
        """
        l_obj = mqttXML._read_one_broker(self.m_xml.broker)
        self.assertEqual(l_obj.Name, TESTING_BROKER_NAME_1)
        self.assertEqual(l_obj.Key, int(TESTING_BROKER_KEY_1))
        self.assertEqual(l_obj.Active, bool(TESTING_BROKER_ACTIVE_1 == 'True'))
        self.assertEqual(l_obj.BrokerAddress, TESTING_BROKER_ADDRESS_1)
        self.assertEqual(l_obj.BrokerPort, int(TESTING_BROKER_PORT_1))

    def test_02_Mqtt(self):
        """Here we should get a dict of brokers
        """
        l_obj = self.m_api.read_mqtt_xml(self.m_pyhouse_obj)
        self.assertEqual(l_obj[0].Name, TESTING_BROKER_NAME_1)
        self.assertEqual(l_obj[0].Key, int(TESTING_BROKER_KEY_1))
        self.assertEqual(l_obj[0].Active, bool(TESTING_BROKER_ACTIVE_1 == 'True'))
        self.assertEqual(l_obj[0].BrokerAddress, TESTING_BROKER_ADDRESS_1)
        self.assertEqual(l_obj[0].BrokerPort, int(TESTING_BROKER_PORT_1))
        self.assertEqual(l_obj[1].Name, TESTING_BROKER_NAME_2)
        self.assertEqual(l_obj[1].Key, int(TESTING_BROKER_KEY_2))
        self.assertEqual(l_obj[1].Active, bool(TESTING_BROKER_ACTIVE_2 == 'True'))
        self.assertEqual(l_obj[1].BrokerAddress, TESTING_BROKER_ADDRESS_2)
        self.assertEqual(l_obj[1].BrokerPort, int(TESTING_BROKER_PORT_2))


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
        self.assertEqual(l_mqtt_obj.BrokerAddress, TESTING_BROKER_ADDRESS_1)
        self.assertEqual(l_xml.attrib['Name'], TESTING_BROKER_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_BROKER_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_BROKER_ACTIVE_1)
        self.assertEqual(l_xml.find('BrokerAddress').text, TESTING_BROKER_ADDRESS_1)
        self.assertEqual(l_xml.find('BrokerPort').text, TESTING_BROKER_PORT_1)

    def test_02_Mqtt(self):
        """Write entire Mqtt XML section
        """
        l_mqtt_obj = self.m_api.read_mqtt_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_mqtt_xml(l_mqtt_obj)
        # PrettyPrintAny(l_xml, 'XML')
        self.assertEqual(l_mqtt_obj[0].BrokerAddress, TESTING_BROKER_ADDRESS_1)
        l_xml1 = l_xml.find('Broker')
        self.assertEqual(l_xml1.attrib['Name'], TESTING_BROKER_NAME_1)
        self.assertEqual(l_xml1.attrib['Key'], TESTING_BROKER_KEY_1)
        self.assertEqual(l_xml1.attrib['Active'], TESTING_BROKER_ACTIVE_1)
        self.assertEqual(l_xml1.find('BrokerAddress').text, TESTING_BROKER_ADDRESS_1)
        self.assertEqual(l_xml1.find('BrokerPort').text, TESTING_BROKER_PORT_1)
        #
        # self.assertEqual(l_xml1.find('BrokerAddress').text, TESTING_BROKER_ADDRESS_2)

# ## END DBK
