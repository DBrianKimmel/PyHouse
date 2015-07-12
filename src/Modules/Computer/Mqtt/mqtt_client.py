"""
-*- test-case-name: PyHouse.Modules.Computer.Mqtt.test.test_computer -*-

@name:      PyHouse/src/Modules/Computer/Mqtt/mqtt_client.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 5, 2015
@Summary:   Connect this computer node to the household Mqtt Broker.

"""

# Import system type stuff
import copy
from twisted.internet.endpoints import clientFromString
from twisted.internet.protocol import ReconnectingClientFactory

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData
from Modules.Computer import logging_pyh as Logger
from Modules.Computer.Mqtt import protocol
from Modules.Computer.Mqtt.mqtt_xml import MqttXmlAPI
from Modules.Web import web_utils

LOG = Logger.getLogger('PyHouse.MqttClient     ')


class Util(object):
    """
    """

    def __init__(self):
        self.m_connection = None

    def mqtt_start(self, p_pyhouse_obj):
        """ Start the async connection process.

        This is the twisted part.
        The connection of the MQTT protocol is kicked off after the TCP connection is complete.
        """
        p_pyhouse_obj.Computer.Mqtt[0].ClientAPI = self
        l_address = p_pyhouse_obj.Computer.Mqtt[0].BrokerAddress
        l_port = p_pyhouse_obj.Computer.Mqtt[0].BrokerPort
        if l_address == None or l_port == None:
            LOG.error('Bad Mqtt broker Address: {}'.format(l_address))
        else:
            p_pyhouse_obj.Twisted.Reactor.connectTCP(l_address, l_port, protocol.MqttClientFactory(p_pyhouse_obj, "DBK1", self))
        # Connect to each of the brokers in the config file.
        for l_broker in p_pyhouse_obj.Computer.Mqtt.itervalues():
            p_pyhouse_obj.Twisted.Reactor.connectTCP(
                l_address,
                l_port,
                protocol.MqttClientFactory(p_pyhouse_obj, "DBK1", self))
            pass

    def client_connect(self, p_pyhouse_obj):
        """
        This will create a connection for each broker in the config file.
        These connections will automatically reconnect if the connection is broken (broker reboots e.g.)
        """
        for l_broker in p_pyhouse_obj.Computer.Mqtt.itervalues():
            l_host = l_broker.BrokerAddress
            l_port = l_broker.BrokerPort
            l_broker_ref = 'tcp:{}:{}'.format(l_host, l_port)
            l_endpoint = clientFromString(
                p_pyhouse_obj.Twisted.Reactor, l_broker_ref)
            pass
        pass


class API(Util):
    """This interfaces to all of PyHouse.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.APIs.Computer.MqttAPI = self

    def Start(self):
        l_config = MqttXmlAPI().read_mqtt_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Mqtt = l_config
        if l_config != {}:
            self.m_mqtt = self.mqtt_start(self.m_pyhouse_obj)
            LOG.info("Broker Started.")
        else:
            LOG.info('No Mqtt broker configured.')

    def Stop(self):
        pass

    def SaveXml(self, p_xml):
        l_xml = MqttXmlAPI().write_mqtt_xml(self.m_pyhouse_obj.Computer.Mqtt)
        p_xml.append(l_xml)
        LOG.info("Saved XML.")
        return p_xml

    def MqttPublish(self, p_topic, p_message):
        """Send a topic, message to the broker for it to distribute to the subscription list

        self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish("pyhouse/schedule/execute", l_schedule_json)

        """
        try:
            self.m_pyhouse_obj.Computer.Mqtt.ProtocolAPI.publish(p_topic, p_message)
        except AttributeError as e_err:
            LOG.error("Unpublished\n   Error:{}\n   Topic:{}\n   Message:{}".format(e_err, p_topic, p_message))

    def MqttDispatch(self, _p_topic, _p_message):
        """Dispatch a MQTT message according to the topic.
        """
        pass

    def doPyHouseLogin(self, p_client, p_pyhouse_obj):
        """Login to PyHouse via MQTT
        """
        self.m_client = p_client
        try:
            l_node = copy.deepcopy(p_pyhouse_obj.Computer.Nodes[0])
        except KeyError:
            l_node = NodeData()
        l_node.NodeInterfaces = None
        l_json = web_utils.JsonUnicode().encode_json(l_node)
        p_client.publish('pyhouse/login/initial', l_json)

# ## END DBK
