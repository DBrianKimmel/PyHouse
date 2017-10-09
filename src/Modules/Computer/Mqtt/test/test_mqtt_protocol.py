"""
@name:      PyHouse/src/Modules/Computer/Mqtt/test/test_protocol.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2015
@Summary:

Passed all 4 tests - DBK- 2017-03-11
"""
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

__updated__ = '2017-04-21'

#  Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from Modules.Computer.Mqtt.test.xml_mqtt import \
    XML_MQTT, \
    TESTING_MQTT_SECTION, \
    TESTING_MQTT_BROKER
from Modules.Computer.test.xml_computer import \
    TESTING_COMPUTER_DIVISION
from Modules.Computer.Mqtt.mqtt_protocol import MQTTProtocol


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_mqtt_protocol')


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Tags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, TESTING_COMPUTER_DIVISION)
        self.assertEqual(self.m_xml.mqtt_sect.tag, TESTING_MQTT_SECTION)
        self.assertEqual(self.m_xml.broker.tag, TESTING_MQTT_BROKER)


class D1_Encode(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))

    def test_01_String(self):
        pass


class P1_Packet(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))

    def test_01_fixed(self):
        l_packet_type = 0x01
        l_remaining_length = 17
        l_fixed = MQTTProtocol()._build_fixed_header(l_packet_type, l_remaining_length)
        # print(PrettyFormatAny.form(l_fixed, 'FixedHeader'))

    def test_02_connect(self):
        """
        """
        l_clientID = "TestClient"
        l_keepalive = 30000
        l_willTopic = None
        l_willMessage = None
        l_willQoS = 0
        l_willRetain = False
        l_cleanStart = True
        l_username = None
        l_password = None

        MQTTProtocol().connect(l_clientID, l_keepalive)
        pass

#  ## END DBK
