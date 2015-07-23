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
# from twisted.internet.endpoints import clientFromString, TCP4ClientEndpoint, connectProtocol
# from twisted.internet.protocol import ReconnectingClientFactory

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData
from Modules.Computer import logging_pyh as Logger
from Modules.Computer.Mqtt import mqtt_protocol
from Modules.Computer.Mqtt.mqtt_xml import MqttXmlAPI
from Modules.Web import web_utils

LOG = Logger.getLogger('PyHouse.Mqtt_Client    ')


class Util(object):
    """
    """

    def __init__(self):
        self.m_connection = None

    '''
    def mqtt_start(self, p_pyhouse_obj):
        """ Start the async connection process.

        This is the twisted part.
        The connection of the MQTT protocol is kicked off after the TCP connection is complete.
        """
        l_count = 0
        p_pyhouse_obj.Computer.Mqtt[0].ClientAPI = self
        l_address = p_pyhouse_obj.Computer.Mqtt[0].BrokerAddress
        l_port = p_pyhouse_obj.Computer.Mqtt[0].BrokerPort
        if l_address == None or l_port == None:
            LOG.error('Bad Mqtt broker Address: {}'.format(l_address))
        else:
            p_pyhouse_obj.Twisted.Reactor.connectTCP(l_address, l_port, mqtt_protocol.MqttClientFactory(p_pyhouse_obj, "DBK1", self))
            l_count += 1
        # Connect to each of the brokers in the config file.
        # for l_broker in p_pyhouse_obj.Computer.Mqtt.itervalues():
        #    p_pyhouse_obj.Twisted.Reactor.connectTCP(
        #        l_address,
        #        l_port,
        #        protocol.MqttClientFactory(p_pyhouse_obj, "DBK1", self))
        return l_count
    '''

    def client_connect_all_brokers(self, p_pyhouse_obj):
        """
        This will create a connection for each broker in the config file.
        These connections will automatically reconnect if the connection is broken (broker reboots e.g.)
        """
        l_count = 0
        for l_broker in p_pyhouse_obj.Computer.Mqtt.itervalues():
            l_host = l_broker.BrokerAddress
            l_port = l_broker.BrokerPort
            l_broker.ClientAPI = self
            if l_host == None or l_port == None:
                LOG.error('Bad Mqtt broker Address: {}'.format(l_host))
                l_broker.ProtocolAPI = None
            else:
                l_factory = mqtt_protocol.MqttReconnectingClientFactory(p_pyhouse_obj, "DBK1", self)
                l_connector = p_pyhouse_obj.Twisted.Reactor.connectTCP(l_host, l_port, l_factory)
                l_broker.ProtocolAPI = l_factory.buildProtocol(l_connector)
                # l_broker_ref = 'tcp:{}:{}'.format(l_host, l_port)
                # l_endpoint = clientFromString(p_pyhouse_obj.Twisted.Reactor, l_broker_ref)
                #    l_endpoint,
                #    mqtt_protocol.MqttReconnectingClientFactory(p_pyhouse_obj, "DBK1", self))
                # l_broker.ProtocolAPI = l_attempt
                l_count += 1
        return l_count


class API(Util):
    """This interfaces to all of PyHouse.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.APIs.Computer.MqttAPI = self

    def Start(self):
        l_config_dict = MqttXmlAPI().read_mqtt_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Mqtt = l_config_dict
        if l_config_dict != {}:
            # l_count = self.mqtt_start(self.m_pyhouse_obj)
            l_count = self.client_connect_all_brokers(self.m_pyhouse_obj)
            LOG.info("Mqtt {} broker(s) Started.".format(l_count))

        else:
            LOG.info('No Mqtt brokers are configured.')

    def Stop(self):
        pass

    def SaveXml(self, p_xml):
        l_xml = MqttXmlAPI().write_mqtt_xml(self.m_pyhouse_obj.Computer.Mqtt)
        p_xml.append(l_xml)
        LOG.info("Saved Mqtt XML.")
        return p_xml

    def MqttPublish(self, p_topic, p_message):
        """Send a topic, message to the broker for it to distribute to the subscription list

        self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish("pyhouse/schedule/execute", l_schedule_json)

        """
        for l_broker in self.m_pyhouse_obj.Computer.Mqtt.itervalues():
            try:
                l_broker.ProtocolAPI.publish(p_topic, p_message)
                LOG.info('Mqtt publishing:\n\t{}\n\t{}'.format(p_topic, p_message))
            except AttributeError as e_err:
                LOG.error("Mqtt Unpublished.\n\tERROR:{}\n\tTopic:{}\n\tMessage:{}".format(e_err, p_topic, p_message))

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
        self.MqttPublish('pyhouse/login/initial', l_json)

# ## END DBK
