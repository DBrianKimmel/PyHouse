"""
@name:      PyHouse/src/Modules/Computer/Mqtt/test/test_mqtt_client.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 5, 2015
@Summary:

Passed all 11 tests - DBK - 2016-01-29

"""

#  Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from twisted.internet import reactor
import twisted
import platform

#  Import PyMh files and modules.
from Modules.Core.data_objects import MqttBrokerData, \
    LocationData, ScheduleLightData, ControllerData
from test.xml_data import XML_LONG, XML_EMPTY
from Modules.Computer.Mqtt.mqtt_client import Util, API as mqttAPI
from test.testing_mixin import SetupPyHouseObj
from Modules.Computer.Mqtt.test.xml_mqtt import \
    TESTING_BROKER_NAME_0, \
    TESTING_BROKER_ACTIVE_0, \
    TESTING_BROKER_KEY_0, \
    TESTING_BROKER_ADDRESS_0, \
    TESTING_BROKER_PORT_0, \
    TESTING_BROKER_NAME_1, \
    TESTING_BROKER_KEY_1, \
    TESTING_BROKER_ADDRESS_1, \
    TESTING_BROKER_PORT_1, \
    TESTING_BROKER_ACTIVE_1
from Modules.Utilities import json_tools
#  from Modules.Utilities.debug_tools import PrettyFormatAny


BROKERv4 = 'iot.eclipse.org'  #  Sandbox Mosquitto broker
BROKER_TLS = '192.168.1.3'
PORT = 1883
PORT_TLS = 8883
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
        except (KeyError, ValueError) as e_err:
            l_val = 'ERRor on JsonPair for key "{}"  {} {}'.format(p_key, e_err, l_json)
            print(l_val)
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

    def test_02_Mqtt(self):
        l_mqtt = self.m_api.LoadXml(self.m_pyhouse_obj)
        self.assertEqual(l_mqtt.Prefix, platform.node())
        self.assertEqual(len(l_mqtt.Brokers), 2)

    def test_03_Broker(self):
        l_mqtt = self.m_api.LoadXml(self.m_pyhouse_obj)
        self.assertEqual(l_mqtt.Brokers[0].Name, TESTING_BROKER_NAME_0)
        self.assertEqual(l_mqtt.Brokers[0].Key, int(TESTING_BROKER_KEY_0))
        self.assertEqual(l_mqtt.Brokers[0].Active, TESTING_BROKER_ACTIVE_0 == 'True')
        self.assertEqual(l_mqtt.Brokers[0].BrokerAddress, TESTING_BROKER_ADDRESS_0)
        self.assertEqual(l_mqtt.Brokers[0].BrokerPort, int(TESTING_BROKER_PORT_0))
        self.assertEqual(l_mqtt.Brokers[1].Name, TESTING_BROKER_NAME_1)
        self.assertEqual(l_mqtt.Brokers[1].Key, int(TESTING_BROKER_KEY_1))
        self.assertEqual(l_mqtt.Brokers[1].Active, TESTING_BROKER_ACTIVE_1 == 'True')
        self.assertEqual(l_mqtt.Brokers[1].BrokerAddress, TESTING_BROKER_ADDRESS_1)
        self.assertEqual(l_mqtt.Brokers[1].BrokerPort, int(TESTING_BROKER_PORT_1))


class A2_EmptyXML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_EMPTY))

    def test_01_Mqtt(self):
        l_mqtt = self.m_api.LoadXml(self.m_pyhouse_obj)
        self.assertEqual(len(l_mqtt.Brokers), 0)


class B1_ConnectTCP(SetupMixin, unittest.TestCase):

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
        self.assertEqual(self.m_broker.Name, 'ClientTest')


class B2_ConnectTLS(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.Twisted.Reactor = reactor
        twisted.internet.base.DelayedCall.debug = True
        self.m_broker.BrokerAddress = BROKER_TLS
        self.m_broker.BrokerPort = PORT_TLS
        self.m_broker.Active = True
        self.m_broker.UserName = 'pyhouse'
        self.m_broker.Password = 'ChangeMe'
        self.m_broker.Name = 'ClientTest'

    def test_01_Broker(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.m_pyhouse_obj.Computer.Mqtt.Brokers = {}
        self.m_pyhouse_obj.Computer.Mqtt.Brokers[0] = self.m_broker
        self.assertEqual(self.m_broker.Name, 'ClientTest')


class C1_Tools(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_02_Obj(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_obj = LocationData()
        l_obj.Street = '123 Test Street'
        l_obj.City = 'Beverly Hills'
        l_obj.State = 'Confusion'
        l_json = json_tools.encode_json(l_obj)
        #  print(PrettyFormatAny.form(l_json, 'Json', 80))


class C2_Publish(SetupMixin, unittest.TestCase):
    """ Test the publish routine.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.Computer.Mqtt.Prefix = "pyhouse/test_house/"
        twisted.internet.base.DelayedCall.debug = True
        self.m_broker.BrokerAddress = BROKERv4
        self.m_broker.BrokerPort = PORT
        self.m_broker.Active = True
        self.m_broker.Name = 'ClientTest'

    def test_01_Topic(self):
        """ Test topic.
        """
        l_topic = Util._make_topic(self.m_pyhouse_obj, 'Test')
        self.assertEqual(l_topic, "pyhouse/test_house/Test")

    def test_02_Message(self):
        """ No payload (not too useful)
        """
        l_message = Util._make_message(self.m_pyhouse_obj)
        #  print(PrettyFormatAny.form(l_message, 'Bare Message', 80))
        self.assertEqual(self.jsonPair(l_message, 'Sender'), self.m_pyhouse_obj.Computer.Name)
        self.assertSubstring('DateTime', l_message)

    def test_03_MessageObj(self):
        """ Add an object.
        """
        l_data = ScheduleLightData()
        l_data.Name = 'Mqtt Controller Object'
        l_data.RoomName = 'Living Room'
        l_data.Comment = 'The formal Living Room.'
        l_message = Util._make_message(self.m_pyhouse_obj, l_data)
        #  print(PrettyFormatAny.form(l_message, 'Message', 80))
        self.assertEqual(self.jsonPair(l_message, 'Sender'), self.m_pyhouse_obj.Computer.Name)
        self.assertSubstring('DateTime', l_message)
        self.assertEqual(self.jsonPair(l_message, 'Name'), l_data.Name)

    def test_04_MessageObj(self):
        """ Add an object.
        """
        l_data = ControllerData()
        l_data.Name = 'Mqtt Schedule Object'
        l_data.LightName = 'Test Light'
        l_data.RoomName = 'Living Room'
        l_data.Comment = 'The formal Living Room.'
        l_message = Util._make_message(self.m_pyhouse_obj, l_data)
        #  print(PrettyFormatAny.form(l_message, 'Message', 80))
        self.assertEqual(self.jsonPair(l_message, 'Sender'), self.m_pyhouse_obj.Computer.Name)
        self.assertSubstring('DateTime', l_message)
        self.assertEqual(self.jsonPair(l_message, 'Name'), l_data.Name)

#  ## END DBK
