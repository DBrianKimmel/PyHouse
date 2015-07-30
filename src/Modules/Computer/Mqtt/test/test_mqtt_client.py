"""
@name:      PyHouse/src/Modules/Computer/Mqtt/test/test_mqtt_client.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 5, 2015
@Summary:

Passed all 2 tests - DBK - 2015-07-23

"""


# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from twisted.internet import reactor
import twisted

# Import PyMh files and modules.
# from Modules.Core.data_objects import MqttBrokerData
from Modules.Core.data_objects import MqttBrokerData
from test.xml_data import XML_LONG
from Modules.Computer.Mqtt.mqtt_client import API as mqttAPI
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny

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


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        """ Be sure that the XML contains the right stuff.
        """
        # PrettyPrintAny(self.m_xml.root, 'XML')
        # PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse_obj')
        pass

    def test_02_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        # PrettyPrintAny(self.m_pyhouse_obj.Xml, 'PyHouse XML')
        # PrettyPrintAny(self.m_xml.root, 'XML')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision', 'XML - No Computer Division')
        self.assertEqual(self.m_xml.mqtt_sect.tag, 'MqttSection', 'XML - No Mqtt section')

    def test_03_Mqtt(self):
        # PrettyPrintAny(self.m_pyhouse_obj.APIs.Computer.MqttAPI, 'Mqtt')
        pass

    def test_05_Mqtt(self):
        # PrettyPrintAny(self.m_pyhouse_obj.Computer, 'Mqtt')
        pass

    def test_06_Broker(self):
        # PrettyPrintAny(self.m_broker, 'Broker')
        pass


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
        self.m_api.client_connect_all_brokers(self.m_pyhouse_obj)

# ## END DBK
