"""
@name:      PyHouse/src/Modules/Computer/Mqtt/test/test_mqtt_client.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 5, 2015
@Summary:

Passed all 7 tests - DBK - 2015-08-12

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from twisted.internet import reactor
import twisted
import platform

# Import PyMh files and modules.
from Modules.Core.data_objects import MqttBrokerData, RoomData, LocationData
from test.xml_data import XML_LONG
from Modules.Computer.Mqtt.mqtt_client import Util, API as mqttAPI
from test.testing_mixin import SetupPyHouseObj
from Modules.Computer.Mqtt.test.xml_mqtt import \
    TESTING_BROKER_NAME_1, \
    TESTING_BROKER_ACTIVE_1, \
    TESTING_BROKER_KEY_1, \
    TESTING_BROKER_ADDRESS_1, \
    TESTING_BROKER_PORT_1, \
    TESTING_BROKER_NAME_2, \
    TESTING_BROKER_KEY_2, \
    TESTING_BROKER_ADDRESS_2, \
    TESTING_BROKER_PORT_2, \
    TESTING_BROKER_ACTIVE_2
from Modules.Housing.test.xml_location import TESTING_LOCATION_CITY
from Modules.Utilities.tools import PrettyPrintAny
from Modules.Utilities import json_tools
from Modules.Utilities.debug_tools import PrettyFormatAny


BROKERv4 = 'iot.eclipse.org'  # Sandbox Mosquitto broker
PORT = 1883
SUBSCRIBE = 'pyhouse/#'


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = mqttAPI(self.m_pyhouse_obj)
        self.m_broker = MqttBrokerData()

    def jsonPair(self, p_json, p_key):
        """ Extract key, value from json
        """
        l_json = json_tools.decode_json_unicode(p_json)
        try:
            l_val = l_json[p_key]
        except KeyError as e_err:
            print('ERROR - {}'.format(e_err))
            l_val = 'ERRor {}'.format(e_err)
        return l_val


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')
        self.assertEqual(self.m_xml.mqtt_sect.tag, 'MqttSection')

    def test_03_Mqtt(self):
        # PrettyPrintAny(self.m_pyhouse_obj.APIs.Computer.MqttAPI, 'Mqtt')
        pass

    def test_05_Mqtt(self):
        l_mqtt = self.m_api.LoadXml()
        self.assertEqual(l_mqtt.Prefix, platform.node())
        self.assertEqual(len(l_mqtt.Brokers), 2)

    def test_06_Broker(self):
        l_mqtt = self.m_api.LoadXml()
        self.assertEqual(l_mqtt.Brokers[0].Name, TESTING_BROKER_NAME_1)
        self.assertEqual(l_mqtt.Brokers[0].Key, int(TESTING_BROKER_KEY_1))
        self.assertEqual(l_mqtt.Brokers[0].Active, TESTING_BROKER_ACTIVE_1 == 'True')
        self.assertEqual(l_mqtt.Brokers[0].BrokerAddress, TESTING_BROKER_ADDRESS_1)
        self.assertEqual(l_mqtt.Brokers[0].BrokerPort, int(TESTING_BROKER_PORT_1))
        self.assertEqual(l_mqtt.Brokers[1].Name, TESTING_BROKER_NAME_2)
        self.assertEqual(l_mqtt.Brokers[1].Key, int(TESTING_BROKER_KEY_2))
        self.assertEqual(l_mqtt.Brokers[1].Active, TESTING_BROKER_ACTIVE_2 == 'True')
        self.assertEqual(l_mqtt.Brokers[1].BrokerAddress, TESTING_BROKER_ADDRESS_2)
        self.assertEqual(l_mqtt.Brokers[1].BrokerPort, int(TESTING_BROKER_PORT_2))


class B1_Connect(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.Twisted.Reactor = reactor
        twisted.internet.base.DelayedCall.debug = True
        self.m_broker.BrokerAddress = BROKERv4
        self.m_broker.BrokerPort = PORT
        self.m_broker.Active = True
        self.m_broker.Name = 'ClientTest'

    def test_01_Broker(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.m_pyhouse_obj.Computer.Mqtt.Brokers = {}
        self.m_pyhouse_obj.Computer.Mqtt.Brokers[0] = self.m_broker
        # PrettyPrintAny(self.m_broker, 'Broker')
        # self.m_api.client_connect_all_brokers(self.m_pyhouse_obj)
        self.assertEqual(self.m_broker.Name, 'ClientTest')

class C1_Tools(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Dict(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_dict = {'Name': 'Test Dict', 'Size': 4, 'Tuple':(1, 'two', True), 'List': [1, 2, 3.4, 5.6]}
        # print(PrettyFormatAny.form(l_dict, 'Dict', 80))
        l_obj = Util._dict2Obj(l_dict)
        # print(PrettyFormatAny.form(l_obj, 'Object', 80))

    def test_02_Obj(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_obj = LocationData()
        l_obj.Street = '123 Test Street'
        l_obj.City = 'Beverly Hills'
        l_obj.State = 'Confusion'
        # print(PrettyFormatAny.form(l_obj, 'Object', 80))
        l_json = json_tools.encode_json(l_obj)
        # print(PrettyFormatAny.form(l_json, 'Json', 80))
        l_ret = Util._json2dict(l_json)
        print(PrettyFormatAny.form(l_ret, 'Json Decoded Object', 80))


class C2_Publish(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.Twisted.Reactor = reactor
        self.m_pyhouse_obj.Computer.Mqtt.Prefix = "pyhouse/test_house/"
        twisted.internet.base.DelayedCall.debug = True
        self.m_broker.BrokerAddress = BROKERv4
        self.m_broker.BrokerPort = PORT
        self.m_broker.Active = True
        self.m_broker.Name = 'ClientTest'

    def test_01_Topic(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_topic = Util._make_topic(self.m_pyhouse_obj, 'Test')
        self.assertEqual(l_topic, "pyhouse/test_house/Test")

    def test_02_Message(self):
        """ No payload
        """
        l_message = Util._make_message(self.m_pyhouse_obj)
        print(l_message)
        self.assertEqual(self.jsonPair(l_message, 'Sender'), self.m_pyhouse_obj.Computer.Name)
        self.assertSubstring('DateTime', l_message)

    def test_03_MessageJson(self):
        """ Add some already encoded Json
        """
        l_data = RoomData()
        l_data.Name = 'Living Room'
        l_data.Comment = 'The formal Living Room.'
        l_json = json_tools.encode_json(l_data)
        l_message = Util._make_message(self.m_pyhouse_obj, message_json = l_json)
        print(PrettyFormatAny.form(l_message, 'Message', 80))
        self.assertEqual(self.jsonPair(l_message, 'Sender'), self.m_pyhouse_obj.Computer.Name)
        self.assertSubstring('DateTime', l_message)
        self.assertEqual(self.jsonPair(l_message, 'Name'), l_data.Name)
        self.assertEqual(self.jsonPair(l_message, 'Comment'), l_data.Comment)
        self.assertEqual(self.jsonPair(l_message, 'Active'), False)

    def test_04_MessageObj(self):
        """ Add an object.
        """
        l_data = RoomData()
        l_data.Name = 'Living Room'
        l_data.Comment = 'The formal Living Room.'
        l_message = Util._make_message(self.m_pyhouse_obj, message_obj = l_data)
        print(l_message)
        self.assertEqual(self.jsonPair(l_message, 'Sender'), self.m_pyhouse_obj.Computer.Name)
        self.assertSubstring('DateTime', l_message)
        self.assertEqual(self.jsonPair(l_message, 'Name'), l_data.Name)

    def test_05_MessageJsonObj(self):
        """ Add some already encoded Json
        """
        l_data = RoomData()
        l_data.Name = 'Living Room'
        l_data.Comment = 'The formal Living Room.'
        l_json = json_tools.encode_json(l_data)
        l_obj = LocationData()
        l_obj.City = 'Beverly Hills'
        l_message = Util._make_message(self.m_pyhouse_obj, message_json = l_json, message_obj = l_obj)
        print(l_message)
        self.assertEqual(self.jsonPair(l_message, 'Sender'), self.m_pyhouse_obj.Computer.Name)
        self.assertSubstring('DateTime', l_message)
        self.assertEqual(self.jsonPair(l_message, 'Name'), l_data.Name)
        self.assertEqual(self.jsonPair(l_message, 'City'), TESTING_LOCATION_CITY)

# ## END DBK
