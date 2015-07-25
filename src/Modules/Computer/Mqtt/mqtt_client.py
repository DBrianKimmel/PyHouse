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

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData
from Modules.Computer.Mqtt import mqtt_protocol
from Modules.Computer.Mqtt.mqtt_xml import Xml as mqttXML
from Modules.Web import web_utils
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Mqtt_Client    ')


class Util(object):
    """
    """

    def __init__(self):
        self.m_connection = None

    def client_connect_all_brokers(self, p_pyhouse_obj):
        """
        This will create a connection for each broker in the config file.
        These connections will automatically reconnect if the connection is broken (broker reboots e.g.)
        """
        l_count = 0
        for l_broker in p_pyhouse_obj.Computer.Mqtt.itervalues():
            if not l_broker.Active:
                continue
            l_host = l_broker.BrokerAddress
            l_port = l_broker.BrokerPort
            l_broker._ClientAPI = self
            if l_host == None or l_port == None:
                LOG.error('Bad Mqtt broker Address: {}'.format(l_host))
                l_broker._ProtocolAPI = None
            else:
                l_factory = mqtt_protocol.MqttReconnectingClientFactory(p_pyhouse_obj, "DBK1", l_broker)
                l_connector = p_pyhouse_obj.Twisted.Reactor.connectTCP(l_host, l_port, l_factory)
                LOG.info('Connected to broker: {}'.format(l_connector))
                l_count += 1
        LOG.info('TCP Connected to {} Broker(s).'.format(l_count))
        return l_count


class API(Util):
    """This interfaces to all of PyHouse.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.APIs.Computer.MqttAPI = self
        LOG.info("Initialized.")

    def Start(self):
        l_config_dict = mqttXML().read_mqtt_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Mqtt = l_config_dict
        if l_config_dict != {}:
            l_count = self.client_connect_all_brokers(self.m_pyhouse_obj)
            LOG.info("Mqtt {} broker(s) Started.".format(l_count))
        else:
            LOG.info('No Mqtt brokers are configured.')

    def Stop(self):
        pass

    def SaveXml(self, p_xml):
        l_xml = mqttXML().write_mqtt_xml(self.m_pyhouse_obj.Computer.Mqtt)
        p_xml.append(l_xml)
        LOG.info("Saved Mqtt XML.")
        return p_xml

    def MqttPublish(self, p_topic, p_message):
        """Send a topic, message to the broker for it to distribute to the subscription list

        self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish("pyhouse/schedule/execute", l_schedule_json)

        """
        for l_broker in self.m_pyhouse_obj.Computer.Mqtt.itervalues():
            if not l_broker.Active:
                continue
            try:
                l_broker._ProtocolAPI.publish(p_topic, p_message)
                LOG.info('Mqtt publishing:\n\tBroker: {}\n\tTopic:{}'.format(l_broker.Name, p_topic))
            except AttributeError as e_err:
                LOG.error("Mqtt Unpublished.\n\tERROR:{}\n\tTopic:{}\n\tMessage:{}".format(e_err, p_topic, p_message))

    def MqttDispatch(self, p_topic, _p_message):
        """Dispatch a received MQTT message according to the topic.
        """
        l_topic = p_topic.split('/')[1:]  # Drop the pyhouse as that is all we subscribed to.
        LOG.info('Dispatch\n\tTopic: {}'.format(l_topic))

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
