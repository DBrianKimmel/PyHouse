"""
@name:      /home/briank/workspace/PyHouse/src/Modules/Computer/Mqtt/test/test_mqtt.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 26, 2017
@summary:   Test

"""

__updated__ = '2017-04-30'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Computer.Mqtt import mqtt
from Modules.Computer.Mqtt.mqtt import API as mqttAPI
from Modules.Computer.test.xml_computer import TESTING_COMPUTER_DIVISION
from Modules.Computer.Mqtt.test.xml_mqtt import TESTING_MQTT_SECTION, TESTING_MQTT_BROKER
from Modules.Core.Utilities.debug_tools import FormatBytes


DICT = {'one': 1, "Two": 'tew'}

class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = mqttAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Mqtt.Prefix = 'pyhouse/'

class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_mqtt_util')


class A1_XML(SetupMixin, unittest.TestCase):

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

class B1_Form(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Topic(self):
        l_topic = mqtt._make_topic(self.m_pyhouse_obj, 'abc/def/ghi')
        print('B1-01-A - {} {}'.format(FormatBytes(l_topic), l_topic))

    def test_02_Msg(self):
        l_msg = mqtt._make_message(self.m_pyhouse_obj, self.m_pyhouse_obj.House)
        print('B1-02-A - {}; {}'.format(FormatBytes(l_msg)[:30], l_msg))

    def test_03_Msg(self):
        l_msg = mqtt._make_message(self.m_pyhouse_obj, DICT)
        print('B1-03-A - {}; {}'.format(FormatBytes(l_msg)[:30], l_msg))

# ## END DBK
