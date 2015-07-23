"""
@name:      PyHouse/src/Modules/Computer/Mqtt/test/test_mqtt_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 4, 2015
@Summary:   Test the read and write of MQTT sections of XML

Passed all 5 tests - DBK - 2015-07-22

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Computer.Mqtt.mqtt_xml import Xml as mqttXML
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
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
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse_obj')

    def test_02_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        PrettyPrintAny(self.m_pyhouse_obj.Xml, 'PyHouse XML')
        # PrettyPrintAny(self.m_xml.root, 'XML')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision', 'XML - No Computer Division')
        self.assertEqual(self.m_xml.mqtt_sect.tag, 'MqttSection', 'XML - No Mqtt section')

    def test_03_Mqtt(self):
        PrettyPrintAny(self.m_xml.mqtt_sect, 'Mqtt')


class B1_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Broker(self):
        """ Read in the xml file and fill in x
        """
        l_xml = self.m_xml.mqtt_sect.find('Broker')
        PrettyPrintAny(l_xml, 'XML')
        l_obj = self.m_api._read_one_broker(l_xml)
        PrettyPrintAny(l_obj, 'Broker')
        self.assertEqual(l_obj.Name, 'iot.eclipse.org')
        self.assertEqual(l_obj.Key, 0, 'No Key')
        self.assertEqual(l_obj.Active, True)

    def test_02_Mqtt(self):
        l_mqtt_obj = self.m_api.read_mqtt_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_mqtt_obj, 'Brokers')
        PrettyPrintAny(l_mqtt_obj[0], 'broker 0')
        PrettyPrintAny(l_mqtt_obj[1], 'broker 1')
        self.assertEqual(l_mqtt_obj[0].BrokerAddress, '1234:5678::dead.beef')
        self.assertEqual(l_mqtt_obj[0].BrokerPort, 1833)


class B2_Write(SetupMixin, unittest.TestCase):
    """
    Test writing out XML pieces of Mqtt info
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Broker(self):
        l_mqtt_obj = self.m_api.read_mqtt_xml(self.m_pyhouse_obj)[0]
        PrettyPrintAny(l_mqtt_obj, 'Obj')
        l_xml = self.m_api._write_one_broker(l_mqtt_obj)
        PrettyPrintAny(l_xml, 'XML')
        self.assertEqual(l_mqtt_obj.BrokerAddress, '1234:5678::dead.beef')

    def test_02_Mqtt(self):
        l_mqtt_obj = self.m_api.read_mqtt_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_mqtt_obj, 'Obj')
        l_xml = self.m_api.write_mqtt_xml(l_mqtt_obj)
        PrettyPrintAny(l_xml, "XML")
        self.assertEqual(l_mqtt_obj[0].BrokerAddress, '1234:5678::dead.beef')

# ## END DBK
