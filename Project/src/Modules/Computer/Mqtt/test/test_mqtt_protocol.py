"""
@name:      PyHouse/src/Modules/Computer/Mqtt/test/test_protocol.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2015
@Summary:

Passed all 5 tests - DBK- 2018-10-02
"""

__updated__ = '2019-06-19'

#  Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from Modules.Computer.Mqtt.mqtt_data import MqttInformation, MqttBrokerInformation
from Modules.Computer.Mqtt.mqtt_protocol import MQTTProtocol
from Modules.Computer.test.xml_computer import \
    TESTING_COMPUTER_DIVISION
from Modules.Computer.Mqtt.test.xml_mqtt import \
    TESTING_MQTT_SECTION, \
    TESTING_MQTT_BROKER
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny, FormatBytes


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


class B1_Packet(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))

    def test_01_String(self):
        pass


class B2_Packet(SetupMixin, unittest.TestCase):
    """
    """
    m_broker = {}

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        self.m_mqtt = MqttInformation()
        self.m_mqtt.ClientID = "TestClient"
        self.m_broker = MqttBrokerInformation()
        self.m_broker.BrokerName = "Test BrokerS"
        self.m_broker.Keepalive = 30000
        self.m_broker.WillTopic = None
        self.m_broker.WillMessage = None
        self.m_broker.WillQoS = 0
        self.m_broker.WillRetain = False
        self.m_broker.CleanStart = True
        self.m_broker.Username = None
        self.m_broker.Password = None

    def test_01_Fixed(self):
        l_packet_type = 0x01
        l_remaining_length = 17
        _l_fixed = MQTTProtocol()._build_fixed_header(l_packet_type, l_remaining_length)
        # print(PrettyFormatAny.form(_l_fixed, 'FixedHeader'))

    def test_02_connect(self):
        """
        """
        l_fixed, l_var, l_pay = MQTTProtocol()._build_connect(self.m_broker, self.m_mqtt)
        # print('\n   Fixed: {}'.format(FormatBytes(l_fixed)))
        # print('Variable: {}'.format(FormatBytes(l_var)))
        # print(' Payload: {}'.format(FormatBytes(l_pay)))
        self.assertEqual(l_fixed, bytearray(b'\x10\x16'))

#  ## END DBK
