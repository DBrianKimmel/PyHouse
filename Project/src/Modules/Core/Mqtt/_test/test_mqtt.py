"""
@name:      Modules/Core/Mqtt/_test/test_mqtt.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 26, 2017
@summary:   Test

Passed all 11 tests - DBK - 2019-08-15

"""

__updated__ = '2019-10-16'

# Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

# Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import PyHouseInformation
from Modules.Core.Mqtt import mqtt
from Modules.Core.Mqtt.mqtt import Api as mqttApi, MqttInformation
from Modules.Core.Utilities import json_tools
from Modules.Computer.computer import ComputerInformation
from Modules.House.Lighting.controllers import ControllerInformation
from Modules.House.Schedule.schedule import ScheduleLightInformation

from Modules.Core.Utilities.debug_tools import FormatBytes, PrettyFormatAny

DICT = {'one': 1, "Two": 'tew'}
LIGHTING_MSG = {
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
TEST_YAML = """\
Mqtt:
    Brokers:
        - Name: Test Broker 1
          Comment: Primary
          Class: Local
          Host:
              Name: mqtt-ct
              Port: 1883
          Access:
              UserName: pyhouse
              Password: pyhouse
          Will:
              Topic: LWT Topic
              Message: Going offline
              Qos: 1
              Retain: false
"""


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_api = mqttApi(self.m_pyhouse_obj, self)
        l_yaml = YAML()
        self.m_test_config = l_yaml.load(TEST_YAML)
        self.m_local_config = mqtt.LocalConfig(self.m_pyhouse_obj)

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
        _x = PrettyFormatAny.form('_test', 'title')  # so it is defined when printing is cleaned up.


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Build(self):
        """ The basic read info as set up
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Core, 'A1-01-B - Computer'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Core.Mqtt, 'A1-01-C - Mqtt'))
        self.assertIsInstance(self.m_pyhouse_obj.Core.Mqtt, MqttInformation)


class C1_YamlRead(SetupMixin, unittest.TestCase):
    """ Read the YAML config files.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Build(self):
        """ The basic read info as set up
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'C1-01-A - PyHouse'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'C1-01-A - Computer'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Core.Mqtt, 'C1-01-B - Mqtt'))
        self.assertIsInstance(self.m_pyhouse_obj, PyHouseInformation)
        self.assertIsInstance(self.m_pyhouse_obj.Computer, ComputerInformation)
        self.assertIsInstance(self.m_pyhouse_obj.Core.Mqtt, MqttInformation)

    def test_02_Broker0(self):
        """ Read the rooms.yaml config file
        """
        l_yaml = self.m_test_config
        # print('C1-02-A - Yaml: ', l_yaml)
        l_mqtt = l_yaml['Mqtt']
        # print('C1-02-B - Mqtt: ', l_mqtt)
        l_brokers = l_mqtt['Brokers']
        # print('C1-02-C - Brokers: ', l_brokers)
        l_broker = l_brokers[0]
        # print('C1-02-D - Broker: ', l_broker)
        l_brk = self.m_local_config._extract_one_broker(l_broker, None)
        print(PrettyFormatAny.form(l_brk, 'C1-02- L - Broker'))
        print(PrettyFormatAny.form(l_brk.Access, 'C1-02-M - Access'))
        print(PrettyFormatAny.form(l_brk.Host, 'C1-02-N - Host'))
        print(PrettyFormatAny.form(l_brk.Will, 'C1-02-O - Will'))
        self.assertEqual(l_brk.Name, 'Test Broker 1')
        self.assertEqual(l_brk.Comment, 'Primary')


class F1_Form(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)
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
        l_data = ScheduleLightInformation()
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
