"""
@name:      PyHouse/src/Modules/Computer/Mqtt/test/test_mqtt_actions.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 11, 2017
@summary:   Test

Passed all 4 tests - DBK - 2017-03-11
"""

__updated__ = '2017-07-07'

#  Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

#  Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Computer.Mqtt.mqtt_actions import Actions as mqtt_actions
from Modules.Computer.test.xml_computer import \
    TESTING_COMPUTER_DIVISION
from Modules.Computer.Mqtt.test.xml_mqtt import \
    TESTING_MQTT_SECTION, \
    TESTING_MQTT_BROKER, XML_MQTT


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
        # print(l_xml)
        self.assertEqual(l_xml.tag, TESTING_MQTT_SECTION)


class B1_Field(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        self.m_get = mqtt_actions(self.m_pyhouse_obj)


    def test_01_HVAC(self):
        l_topic = 'pyhouse/pink poppy/irrigation'
        l_payload = '{"DateTime": "2017-07-07 10:45:02.464763", "Sender": "briank-Laptop-3"}'
        print(l_topic)
        print(l_payload)
        l_sender = self.m_get._get_field(l_payload, 'Sender')
        print(l_sender)
        # self.assertEqual(l_raw[:13], '<MqttSection>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_MQTT)
        # print(l_xml)
        self.assertEqual(l_xml.tag, TESTING_MQTT_SECTION)

# ## END DBK
