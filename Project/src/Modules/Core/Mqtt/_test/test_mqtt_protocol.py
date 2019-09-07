"""
@name:      Modules/Core/Mqtt/_test/test_protocol.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2015
@Summary:

Passed all 4 tests - DBK- 2019-08-015
"""

__updated__ = '2019-08-15'

#  Import system type stuff
from twisted.trial import unittest

#  Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.Mqtt.mqtt import MqttInformation, MqttBrokerInformation
from Modules.Core.Mqtt.mqtt_protocol import MQTTProtocol
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_mqtt_protocol')


class B1_Packet(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_String(self):
        pass


class B2_Packet(SetupMixin, unittest.TestCase):
    """
    """
    m_broker = {}

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_mqtt = MqttInformation()
        self.m_mqtt.ClientID = "TestClient"
        self.m_broker = MqttBrokerInformation()
        self.m_broker.BrokerName = "Test BrokerS"
        self.m_broker.Keepalive = 30000
        self.m_broker.WillTopic = None
        self.m_broker.WillMessage = None
        self.m_broker.WillQoS = 0
        self.m_broker.WillRetain = False
        self.m_broker.CleanStart = True
        self.m_broker.Username = None
        self.m_broker.Password = None

    def test_01_Fixed(self):
        l_packet_type = 0x01
        l_remaining_length = 17
        _l_fixed = MQTTProtocol()._build_fixed_header(l_packet_type, l_remaining_length)
        # print(PrettyFormatAny.form(_l_fixed, 'FixedHeader'))

    def test_02_connect(self):
        """
        """
        l_fixed, l_var, l_pay = MQTTProtocol()._build_connect(self.m_broker, self.m_mqtt)
        # print('\n   Fixed: {}'.format(FormatBytes(l_fixed)))
        # print('Variable: {}'.format(FormatBytes(l_var)))
        # print(' Payload: {}'.format(FormatBytes(l_pay)))
        self.assertEqual(l_fixed, bytearray(b'\x10\x16'))

#  ## END DBK
