"""
@name:      PyHouse/Project/src/Modules/Computer/Mqtt/_test/test_mqtt.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 26, 2017
@summary:   Test

Passed all 11 tests - DBK - 2019-07-01

"""

__updated__ = '2019-07-24'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import \
    ScheduleLightData, \
    ControllerInformation, \
    PyHouseInformation, \
    ComputerInformation
from Modules.Core.Mqtt import mqtt
from Modules.Core.Mqtt.mqtt import \
    API as mqttAPI, \
    Yaml as mqttYaml
from Modules.Core.Mqtt.mqtt_data import MqttInformation
from Modules.Computer.test.xml_computer import TESTING_COMPUTER_DIVISION
from Modules.Core.Mqtt.test.xml_mqtt import TESTING_MQTT_SECTION, TESTING_MQTT_BROKER
from Modules.Core.Utilities import json_tools, config_tools

from Modules.Core.Utilities.debug_tools import FormatBytes, PrettyFormatAny

DICT = {'one': 1, "Two": 'tew'}
LIGHTING_MSG = \
{
    'Active': True,
    'BaudRate': 19200,
    'ByteSize': 8,
    'Comment': 'Mobile Version',
    'DateTime': '2019-01-27 17:23:57.988185',
    'DevCat': 288,
    'DeviceFamily': 'Insteon',
    'DeviceSubType': 2,
    'DeviceType': 'Lighting',
    'DsrDtr': False,
    'EngineVersion': 0,
    'FirmwareVersion': 0,
    'GroupList': None,
    'GroupNumber': 0,
    'InsteonAddress': 3757095,
    'InterfaceType': 'Serial',
    'Key': 3,
    'LastUpdate': '2019-01-11 16:38:20.788302',
    'LasuUsed': None,
    'Links': {},
    'Name': 'PLM_3',
    'Node': None,
    'Parity': 'N',
    'Port': '/dev/ttyUSB0',
    'ProductKey': 0,
    'Ret': None,
    'RoomCoords': {'X_Easting': 0.0, 'Y_Northing': 0.0, 'Z_Height': 0.0},
    'RoomName': 'Mobile',
    'RoomUUID': 'c894ef92-b1e5-11e6-8a14-74da3859e09a',
    'RtsCts': False,
    'Sender': 'Laptop-3',
    'StopBits': 1.0,
    'Timeout': 1.0,
    'UUID': 'c1490758-092e-3333-bffa-b827eb189eb4',
    'XonXoff': False
}
DATE_TIME = "2017-03-11 10:45:02.464763"
SENDER = "Laptop-3"

MSG = "{ \
        'Active': True, \
        'Comment': '', \
        'ConnectionAddr_IPv4': [], \
        'ConnectionAddr_IPv6': [\
            ['::1'], \
            ['fe80::72b7:3dcc:f8c8:41ba%eth0'], \
            ['fe80::83cd:6fcd:6c62:638d%wlan0']\
        ], \
        'ControllerCount': 1, \
        'ControllerTypes': ['Insteon'], \
        'DateTime': '2019-01-27 14:07:50.633413', \
        'Key': 2, \
        'LastUpdate': '2019-01-27 12:18:28.041302', \
        'Name': 'pi-01-pp', \
        'NodeId': None, \
        'NodeInterfaces': None, \
        'NodeRole': 0, \
        'Sender': 'pi-01-pp', \
        'UUID': 'd8ec093e-e4a8-11e6-b6ac-74da3859e09a' \
    }"


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = mqttAPI(self.m_pyhouse_obj, self)
        self.m_filename = 'mqtt.yaml'

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

    def test_00_Print(self):
        print('Id: test_mqtt_util')
        _w = FormatBytes('123')
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.Core.Mqtt.Prefix = "pyhouse/test_house/"

    def test_01_Tags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, TESTING_COMPUTER_DIVISION)
        self.assertEqual(self.m_xml.mqtt_sect.tag, TESTING_MQTT_SECTION)
        self.assertEqual(self.m_xml.broker.tag, TESTING_MQTT_BROKER)


class C1_YamlRead(SetupMixin, unittest.TestCase):
    """ Read the YAML config files.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_yaml = mqttYaml(self.m_pyhouse_obj)
        self.m_working_rooms = self.m_pyhouse_obj.Core.Mqtt

    def test_01_Build(self):
        """ The basic read info as set up
        """
        # print(PrettyFormatAny.form(self.m_working_rooms, 'C1-01-A - WorkingRooms'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'C1-01-A - Computer'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Core.Mqtt, 'C1-01-B - Mqtt'))
        self.assertIsInstance(self.m_pyhouse_obj, PyHouseInformation)
        self.assertIsInstance(self.m_pyhouse_obj.Computer, ComputerInformation)
        self.assertIsInstance(self.m_pyhouse_obj.Core.Mqtt, MqttInformation)

    def test_02_ReadFile(self):
        """ Read the rooms.yaml config file
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_yaml = l_node.Yaml
        l_first = config_tools.Yaml(self.m_pyhouse_obj).find_first_element(l_yaml)
        l_yaml_top = l_yaml['Mqtt']
        # print(PrettyFormatAny.form(l_node, 'C1-02-A - Node'))
        # print(PrettyFormatAny.form(l_yaml, 'C1-02-B - Yaml'))
        # print(PrettyFormatAny.form(l_yaml_top, 'C1-02-C - Yaml_top'))
        # print(PrettyFormatAny.form(l_yaml_top[0], 'C1-02-D - Yaml_top[0]'))
        self.assertEqual(l_first, 'Mqtt')
        self.assertEqual(l_yaml_top[0]['Broker']['Name'], 'Test Broker 1')
        self.assertEqual(len(l_yaml_top), 2)

    def test_03_Broker(self):
        """ Extract one broker
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_yaml = l_node.Yaml['Mqtt']
        l_first_broker = config_tools.Yaml(self.m_pyhouse_obj).find_first_element(l_yaml)
        l_broker = self.m_yaml._extract_broker(l_first_broker, self)
        print('C1-03-A - Yaml: {}'.format(l_first_broker))
        print(PrettyFormatAny.form(l_broker, 'C1-03-B - Broker'))
        self.assertEqual(l_broker.Name, 'Test Broker 1')
        self.assertEqual(l_broker.Active, 'True')


class F1_Form(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.Core.Mqtt.Prefix = "pyhouse/test_house/"

    def test_01_Topic(self):
        """ Test topic.
        """
        _l_topic = mqtt._make_topic(self.m_pyhouse_obj, 'Test')
        self.assertEqual(_l_topic, "pyhouse/test_house/Test")

    def test_02_Topic(self):
        _l_topic = mqtt._make_topic(self.m_pyhouse_obj, 'abc/def/ghi')
        # print('B1-02-A - {} {}'.format(FormatBytes(l_topic), l_topic))

    def test_03_Msg(self):
        _l_msg = mqtt._make_message(self.m_pyhouse_obj, self.m_pyhouse_obj.House)
        # print('B1-03-A - {}; {}'.format(FormatBytes(l_msg)[:300], l_msg))

    def test_04_Msg(self):
        _l_msg = mqtt._make_message(self.m_pyhouse_obj, DICT)
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
        l_data = ControllerInformation()
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
