"""
@name:      PyHouse/src/Modules/Computer/Mqtt/test/test_mqtt_client.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 5, 2015
@Summary:

Passed all 14 tests - DBK - 2017-04-21

"""
__updated__ = '2017-04-21'

#  Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from twisted.internet import reactor
import twisted

#  Import PyMh files and modules.
from test.xml_data import XML_LONG, XML_EMPTY, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import MqttBrokerData, \
    LocationData, ScheduleLightData, ControllerData, \
    ComputerInformation
from Modules.Computer.Mqtt.mqtt_client import Util, API as mqttAPI
from Modules.Computer.Mqtt.test.xml_mqtt import \
    TESTING_BROKER_NAME_1, \
    TESTING_BROKER_ACTIVE_1
from Modules.Core.Utilities import json_tools
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


BROKERv4 = 'iot.eclipse.org'  #  Sandbox Mosquitto broker
BROKER_TLS = '192.168.1.10'
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


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_mqtt_client')


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_Tags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-1-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')
        self.assertEqual(self.m_xml.mqtt_sect.tag, 'MqttSection')


class A2_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BrokerCnt(self):
        l_xml = self.m_xml.mqtt_sect
        # print(PrettyFormatAny.form(l_xml, 'A2-1-A - Xml'))
        self.assertEqual(len(l_xml), 2)

    def test_02_PyHouse(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A2_2_A - PyHouse'))
        self.assertIsInstance(self.m_pyhouse_obj.Computer, ComputerInformation)
        self.assertIsInstance(self.m_pyhouse_obj.Computer, ComputerInformation)

    def test_03_Computer(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'A2_3_A - Init Computer'))
        pass

    def test_04_Mqtt(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer.Mqtt, 'A2_4_A - Init Mqtt'))
        pass


class A3_EmptyXML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_EMPTY))

    def test_01_Mqtt(self):
        l_mqtt = self.m_api.LoadXml(self.m_pyhouse_obj)
        self.assertEqual(len(l_mqtt.Brokers), 0)


class B1_TcpConnect(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.Twisted.Reactor = reactor
        # twisted.internet.base.DelayedCall.debug = True
        self.m_broker.BrokerAddress = BROKERv4
        self.m_broker.BrokerPort = PORT
        self.m_broker.Active = TESTING_BROKER_ACTIVE_1
        self.m_broker.Name = TESTING_BROKER_NAME_1

    def test_01_Broker(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.m_pyhouse_obj.Computer.Mqtt.Brokers = {}
        self.m_pyhouse_obj.Computer.Mqtt.Brokers[0] = self.m_broker
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer.Mqtt.Brokers, 'B1-01-A - Broker', 80))
        self.assertEqual(self.m_broker.Name, TESTING_BROKER_NAME_1)


class B2_ConnectTLS(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.Twisted.Reactor = reactor
        # twisted.internet.base.DelayedCall.debug = True
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
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer.Mqtt.Brokers, 'B2-01-A - Broker', 80))
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
        _l_json = json_tools.encode_json(l_obj)
        #  print(PrettyFormatAny.form(l_json, 'Json', 80))


class C2_Publish(SetupMixin, unittest.TestCase):
    """ Test the publish routine.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.Computer.Mqtt.Prefix = "pyhouse/test_house/"
        # twisted.internet.base.DelayedCall.debug = True
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
        # print(PrettyFormatAny.form(l_message, 'C2-02-A - Bare Message', 80))
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
        # print(PrettyFormatAny.form(l_message, 'C2-03-A - Message', 80))
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
        # print(PrettyFormatAny.form(l_message, 'C2-04-A - Message', 80))
        self.assertEqual(self.jsonPair(l_message, 'Sender'), self.m_pyhouse_obj.Computer.Name)
        self.assertSubstring('DateTime', l_message)
        self.assertEqual(self.jsonPair(l_message, 'Name'), l_data.Name)

#  ## END DBK
