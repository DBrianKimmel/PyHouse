"""
@name:      /home/briank/workspace/PyHouse/src/Modules/Computer/Mqtt/test/test_mqtt.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 26, 2017
@summary:   Test

Passed all 9 tests - DBK - 2018-02-11

"""

__updated__ = '2018-02-11'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import ScheduleLightData, ControllerData
from Modules.Computer.Mqtt import mqtt
from Modules.Computer.Mqtt.mqtt import API as mqttAPI
from Modules.Computer.test.xml_computer import TESTING_COMPUTER_DIVISION
from Modules.Computer.Mqtt.test.xml_mqtt import TESTING_MQTT_SECTION, TESTING_MQTT_BROKER
from Modules.Core.Utilities import json_tools
from Modules.Core.Utilities.debug_tools import FormatBytes

DICT = {'one': 1, "Two": 'tew'}


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = mqttAPI(self.m_pyhouse_obj)

    def jsonPair(self, p_json, p_key):
        """ Extract key, value from json
        """
        l_json = json_tools.decode_json_unicode(p_json)
        try:
            l_val = l_json[p_key]
        except (KeyError, ValueError) as e_err:
            l_val = 'ERRor on JsonPair for key "{}"  {} {}'.format(p_key, e_err, l_json)
            print(l_val)
        return l_val


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_mqtt_util')


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.Computer.Mqtt.Prefix = "pyhouse/test_house/"

    def test_01_Tags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, TESTING_COMPUTER_DIVISION)
        self.assertEqual(self.m_xml.mqtt_sect.tag, TESTING_MQTT_SECTION)
        self.assertEqual(self.m_xml.broker.tag, TESTING_MQTT_BROKER)


class B1_Form(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.Computer.Mqtt.Prefix = "pyhouse/test_house/"

    def test_01_Topic(self):
        """ Test topic.
        """
        l_topic = mqtt._make_topic(self.m_pyhouse_obj, 'Test')
        self.assertEqual(l_topic, "pyhouse/test_house/Test")

    def test_02_Topic(self):
        l_topic = mqtt._make_topic(self.m_pyhouse_obj, 'abc/def/ghi')
        # print('B1-02-A - {} {}'.format(FormatBytes(l_topic), l_topic))

    def test_03_Msg(self):
        l_msg = mqtt._make_message(self.m_pyhouse_obj, self.m_pyhouse_obj.House)
        # print('B1-03-A - {}; {}'.format(FormatBytes(l_msg)[:300], l_msg))

    def test_04_Msg(self):
        l_msg = mqtt._make_message(self.m_pyhouse_obj, DICT)
        # print('B1-04-A - {}; {}'.format(FormatBytes(l_msg)[:30], l_msg))

    def test_05_Message(self):
        """ No payload (not too useful)
        """
        l_message = mqtt._make_message(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_message, 'B1-05-A - Bare Message', 80))
        self.assertEqual(self.jsonPair(l_message, 'Sender'), self.m_pyhouse_obj.Computer.Name)
        self.assertSubstring('DateTime', l_message)

    def test_06_MessageObj(self):
        """ Add an object.
        """
        l_data = ScheduleLightData()
        l_data.Name = 'Mqtt Controller Object'
        l_data.RoomName = 'Living Room'
        l_data.Comment = 'The formal Living Room.'
        l_message = mqtt._make_message(self.m_pyhouse_obj, l_data)
        # print(PrettyFormatAny.form(l_message, 'C2-03-A - Message', 80))
        self.assertEqual(self.jsonPair(l_message, 'Sender'), self.m_pyhouse_obj.Computer.Name)
        self.assertSubstring('DateTime', l_message)
        self.assertEqual(self.jsonPair(l_message, 'Name'), l_data.Name)

    def test_07_MessageObj(self):
        """ Add an object.
        """
        l_data = ControllerData()
        l_data.Name = 'Mqtt Schedule Object'
        l_data.LightName = 'Test Light'
        l_data.RoomName = 'Living Room'
        l_data.Comment = 'The formal Living Room.'
        l_message = mqtt._make_message(self.m_pyhouse_obj, l_data)
        # print(PrettyFormatAny.form(l_message, 'C2-04-A - Message', 80))
        self.assertEqual(self.jsonPair(l_message, 'Sender'), self.m_pyhouse_obj.Computer.Name)
        self.assertSubstring('DateTime', l_message)
        self.assertEqual(self.jsonPair(l_message, 'Name'), l_data.Name)

# ## END DBK
