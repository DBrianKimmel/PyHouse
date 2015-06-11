"""
@name:      PyHouse/src/Modules/Computer/Mqtt/test/test_mqtt_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@Copyright: (c)  2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 4, 2015
@Summary:   Test the read and write of MQTT sections of XML

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
# from Modules.Core.data_objects import MqttBrokerData
from test import xml_data
# from test.xml_data import *
from Modules.Computer.Mqtt import mqtt_xml
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = mqtt_xml.ReadWriteConfigXml()


class C01_XML(SetupMixin, unittest.TestCase):
    """
    Test Staticmethods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        # PrettyPrintAny(self.m_xml.root, 'XML')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision', 'XML - No Computer Division')
        self.assertEqual(self.m_xml.mqtt_sect.tag, 'MqttSection', 'XML - No Mqtt section')
        PrettyPrintAny(self.m_pyhouse_obj.Xml, 'XML')
        PrettyPrintAny(self.m_xml.mqtt_sect, 'Mqtt')


class C02_Read(SetupMixin, unittest.TestCase):
    """
    Test Staticmethods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_Base(self):
        """ Read in the xml file and fill in x
        """
        l_mqtt_obj = self.m_api._read_one_broker(self.m_xml.broker)
        PrettyPrintAny(self.m_xml.mqtt_sect)
        PrettyPrintAny(l_mqtt_obj)
        self.assertEqual(l_mqtt_obj.Name, 'iot.eclipse.org')
        self.assertEqual(l_mqtt_obj.Key, 0, 'No Key')
        self.assertEqual(l_mqtt_obj.Active, True)

    def test_02_Broker(self):
        l_mqtt_obj = self.m_api.read_mqtt_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_mqtt_obj[0])
        self.assertEqual(l_mqtt_obj[0].BrokerAddress, '1234:5678::dead.beef')
        self.assertEqual(l_mqtt_obj[0].BrokerPort, 1833)


class C03_Write(SetupMixin, unittest.TestCase):
    """
    Test Staticmethods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_Base(self):
        """ Read in the xml file and fill in x
        """
        l_mqtt_obj = self.m_api._read_one_broker(self.m_xml.mqtt_sect)
        PrettyPrintAny(l_mqtt_obj)
        self.assertEqual(l_mqtt_obj.Name, 'Evening 1')
        self.assertEqual(l_mqtt_obj.Key, 0, 'No Key')
        self.assertEqual(l_mqtt_obj.Active, 0, 'No Active')

    def test_02_Broker(self):
        l_mqtt_obj = self.m_api.read_mqtt_xml(self.m_pyhouse_obj)
        self.assertEqual(l_mqtt_obj[0].BrokerAddress, '1234:5678::dead.beef')

# ## END DBK
