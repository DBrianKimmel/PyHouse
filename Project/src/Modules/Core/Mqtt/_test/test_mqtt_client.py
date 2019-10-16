"""
@name:      Modules/Core/Mqtt/_test/test_mqtt_client.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 5, 2015
@Summary:

Passed all 7 tests - DBK - 2019-08-15

"""

__updated__ = '2019-10-16'

#  Import system type stuff
from twisted.trial import unittest
from twisted.internet import reactor

#  Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities import json_tools
from Modules.Core.Mqtt.mqtt import _make_message, MqttBrokerInformation
from Modules.House.Lighting.controllers import ControllerInformation
from Modules.House.house_data import LocationInformation
from Modules.House.Lighting.lighting import ScheduleLightingInformation

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

BROKERv4 = 'iot.eclipse.org'  #  Sandbox Mosquitto broker
BROKER_TLS = '192.168.1.10'
PORT = 1883
PORT_TLS = 8883
SUBSCRIBE = 'pyhouse/#'


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_broker = MqttBrokerInformation()

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
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_mqtt_client')


class C1_TcpConnect(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_pyhouse_obj._Twisted.Reactor = reactor
        # twisted.internet.base.DelayedCall.debug = True
        self.m_broker.BrokerAddress = BROKERv4
        self.m_broker.Host.Port = PORT
        # self.m_broker.Name = TESTING_BROKER_NAME_1

    def test_01_Broker(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.m_pyhouse_obj.Core.Mqtt.Brokers = {}
        self.m_pyhouse_obj.Core.Mqtt.Brokers[0] = self.m_broker
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Core.Mqtt.Brokers, 'B1-01-A - Broker', 80))
        # self.assertEqual(self.m_broker.Name, TESTING_BROKER_NAME_1)


class C2_ConnectTLS(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_pyhouse_obj._Twisted.Reactor = reactor
        # twisted.internet.base.DelayedCall.debug = True
        self.m_broker.BrokerAddress = BROKER_TLS
        self.m_broker.Host.Port = PORT_TLS
        self.m_broker.Active = True
        self.m_broker.Access.UserName = 'pyhouse'
        self.m_broker.Access.Password = 'ChangeMe'
        self.m_broker.Name = 'ClientTest'

    def test_01_Broker(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.m_pyhouse_obj.Core.Mqtt.Brokers = {}
        self.m_pyhouse_obj.Core.Mqtt.Brokers[0] = self.m_broker
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Core.Mqtt.Brokers, 'B2-01-A - Broker', 80))
        self.assertEqual(self.m_broker.Name, 'ClientTest')


class D1_Tools(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)

    def test_02_Obj(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_obj = LocationInformation()
        l_obj.Street = '123 Test Street'
        l_obj.City = 'Beverly Hills'
        l_obj.State = 'Confusion'
        _l_json = json_tools.encode_json(l_obj)
        #  print(PrettyFormatAny.form(l_json, 'Json', 80))


class C2_Publish(SetupMixin, unittest.TestCase):
    """ Test the publish routine.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_pyhouse_obj.Core.Mqtt.Prefix = "pyhouse/test_house/"
        # twisted.internet.base.DelayedCall.debug = True
        self.m_broker.BrokerAddress = BROKERv4
        self.m_broker.Host.Port = PORT
        self.m_broker.Active = True
        self.m_broker.Name = 'ClientTest'

    def test_02_Message(self):
        """ No payload (not too useful)
        """
        l_message = _make_message(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_message, 'C2-02-A - Bare Message', 80))
        self.assertEqual(self.jsonPair(l_message, 'Sender'), self.m_pyhouse_obj.Computer.Name)
        self.assertSubstring('DateTime', l_message)

    def test_03_MessageObj(self):
        """ Add an object.
        """
        l_data = ScheduleLightingInformation()
        l_data.Name = 'Mqtt Controller Object'
        l_data.RoomName = 'Living Room'
        l_data.Comment = 'The formal Living Room.'
        l_message = _make_message(self.m_pyhouse_obj, l_data)
        # print(PrettyFormatAny.form(l_message, 'C2-03-A - Message', 80))
        self.assertEqual(self.jsonPair(l_message, 'Sender'), self.m_pyhouse_obj.Computer.Name)
        self.assertSubstring('DateTime', l_message)
        self.assertEqual(self.jsonPair(l_message, 'Name'), l_data.Name)

    def test_04_MessageObj(self):
        """ Add an object.
        """
        l_data = ControllerInformation()
        l_data.Name = 'Mqtt Schedule Object'
        l_data.LightName = 'Test Light'
        l_data.RoomName = 'Living Room'
        l_data.Comment = 'The formal Living Room.'
        l_message = _make_message(self.m_pyhouse_obj, l_data)
        # print(PrettyFormatAny.form(l_message, 'C2-04-A - Message', 80))
        self.assertEqual(self.jsonPair(l_message, 'Sender'), self.m_pyhouse_obj.Computer.Name)
        self.assertSubstring('DateTime', l_message)
        self.assertEqual(self.jsonPair(l_message, 'Name'), l_data.Name)

#  ## END DBK
