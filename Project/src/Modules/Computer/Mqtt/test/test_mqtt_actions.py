"""
@name:      PyHouse/src/Modules/Computer/Mqtt/test/test_mqtt_actions.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 11, 2017
@summary:   Test

Passed all 6 tests - DBK - 2017-12-28
"""

__updated__ = '2018-10-02'

#  Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

#  Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Computer.computer import API as computerAPI
from Modules.Housing.house import API as houseAPI
from Modules.Computer.Mqtt.mqtt_actions import Actions as mqtt_actions
from Modules.Computer.test.xml_computer import \
    TESTING_COMPUTER_DIVISION
from Modules.Computer.Mqtt.test.xml_mqtt import \
    TESTING_MQTT_SECTION, \
    TESTING_MQTT_BROKER, XML_MQTT
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

DATE_TIME = "2017-03-11 10:45:02.464763"
SENDER = "Laptop-3"


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_mqtt_actions')


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


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_MQTT
        # print(l_raw)
        self.assertEqual(l_raw[:13], '<MqttSection>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_MQTT)
        # print(PrettyFormatAny.form(l_xml, 'A2-01-A - Parsed'))
        self.assertEqual(l_xml.tag, TESTING_MQTT_SECTION)


class B1_Field(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        self.m_get = mqtt_actions(self.m_pyhouse_obj)

    def test_01_HVAC(self):
        l_topic = 'pyhouse/pink poppy/irrigation'
        l_payload = {"DateTime": DATE_TIME, "Sender": SENDER}
        l_sender = self.m_get._get_field(l_payload, 'Sender')
        # print("\n\tTopic: {}\n\tPayload: {}".format(l_topic, l_payload))
        self.assertEqual(l_sender, SENDER)


class B2_Dispatch(SetupMixin, unittest.TestCase):
    """ Testing of the mqtt_dispatch routine
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        self.m_get = mqtt_actions(self.m_pyhouse_obj)

    def test_01_Computer(self):
        l_topic = 'computer/xml'
        l_payload = {"DateTime": DATE_TIME, "Sender": SENDER}
        self.m_pyhouse_obj.APIs.ComputerAPI = computerAPI(self.m_pyhouse_obj)
        # print("\n\tTopic: {}\n\tPayload: {}".format(l_topic, l_payload))
        l_log = mqtt_actions(self.m_pyhouse_obj).mqtt_dispatch(l_topic, l_payload)
        # print("\t--Log: {}\n".format(l_log))
        # self.assertEqual(l_topic[:13], '<MqttSection>')
        self.assertEqual(l_log[:13], '<MqttSection>')

    def test_02_House(self):
        l_topic = list(['house', ''])
        l_payload = {"DateTime": DATE_TIME, "Sender": SENDER}
        self.m_pyhouse_obj.APIs.HouseAPI = houseAPI(self.m_pyhouse_obj)
        # print("\n\tTopic: {}\n\tPayload: {}".format(l_topic, l_payload))
        l_log = mqtt_actions(self.m_pyhouse_obj).mqtt_dispatch(l_topic, l_payload)
        # print("\t--Log: {}\n".format(l_log))
        # self.assertEqual(l_raw[:13], '<MqttSection>')

# ## END DBK
