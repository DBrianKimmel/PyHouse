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
import datetime
from collections import namedtuple

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData, MqttInformation, MqttJson
from Modules.Computer.Mqtt.mqtt_protocol import PyHouseMqttFactory
from Modules.Computer.Mqtt.mqtt_xml import Xml as mqttXML
from Modules.Web import web_utils
from Modules.Utilities import json_tools, xml_tools
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities.debug_tools import PrettyFormatAny

LOG = Logger.getLogger('PyHouse.Mqtt_Client    ')


class Struct:
    def __init__(self, **args):
        self.__dict__.update(args)


class Util(object):
    """
    """

    def client_connect_all_brokers(self, p_pyhouse_obj):
        """
        This will create a connection for each broker in the config file.
        These connections will automatically reconnect if the connection is broken (broker reboots e.g.)
        """
        l_count = 0
        for l_broker in p_pyhouse_obj.Computer.Mqtt.Brokers.itervalues():
            if not l_broker.Active:
                continue
            l_host = l_broker.BrokerAddress
            l_port = l_broker.BrokerPort
            l_broker._ClientAPI = self
            if l_host == None or l_port == None:
                LOG.error('Bad Mqtt broker Address: {}'.format(l_host))
                l_broker._ProtocolAPI = None
            else:
                l_factory = PyHouseMqttFactory(p_pyhouse_obj, "DBK1", l_broker)
                _l_connector = p_pyhouse_obj.Twisted.Reactor.connectTCP(l_host, l_port, l_factory)
                LOG.info('Connected to broker: {}'.format(l_broker.Name))
                l_count += 1
        LOG.info('TCP Connected to {} Broker(s).'.format(l_count))
        return l_count

    @staticmethod
    def _make_topic(p_pyhouse_obj, p_topic):
        l_topic = p_pyhouse_obj.Computer.Mqtt.Prefix + p_topic
        return l_topic

    @staticmethod
    def _dict2Obj(p_dict):
        """Convert a dict to an Object.
        """
        l_obj = namedtuple('MyObj', p_dict)
        return l_obj

    @staticmethod
    def _json2dict(p_json):
        """Convert JSON to Obj.
        """
        l_ret = json_tools.decode_json_unicode(p_json)
        return l_ret

    @staticmethod
    def _make_message(p_pyhouse_obj, message_json = None, message_obj = None):
        """
        @param p_pyhouse_obj: is the entire PyHouse Data tree.
        @param message_json: is message that is already json encoded\
        @param message_obj: is additional object that will be added into the meddage as Json.
        """
        l_message = MqttJson()
        l_message.Sender = p_pyhouse_obj.Computer.Name
        l_message.DateTime = datetime.datetime.now()
        if message_json != None:
            l_dict = Util._json2dict(message_json)
            l_tmp = Struct(**l_dict)
            xml_tools.stuff_new_attrs(l_message, l_tmp)
            # print(l_tmp)
        if message_obj != None:
            xml_tools.stuff_new_attrs(l_message, message_obj)
        l_json = json_tools.encode_json(l_message)
        return l_json


class API(Util):
    """This interfaces to all of PyHouse.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.APIs.Computer.MqttAPI = self
        p_pyhouse_obj.Computer.Mqtt = MqttInformation()
        p_pyhouse_obj.Computer.Mqtt.Prefix = 'ReSeT'
        p_pyhouse_obj.Computer.Mqtt.Brokers = {}
        LOG.info("Initialized.")

    def Start(self):
        self.m_pyhouse_obj.Computer.Mqtt = self.LoadXml()
        if self.m_pyhouse_obj.Computer.Mqtt.Brokers != {}:
            l_count = self.client_connect_all_brokers(self.m_pyhouse_obj)
            LOG.info("Mqtt {} broker(s) Started.".format(l_count))
        else:
            LOG.info('No Mqtt brokers are configured.')

    def Stop(self):
        pass

    def LoadXml(self):
        """ Load the Mqtt xml info.
        """
        l_mqtt = MqttInformation()
        l_mqtt.Prefix = self.m_pyhouse_obj.Computer.Name
        l_mqtt.Brokers = mqttXML.read_mqtt_xml(self.m_pyhouse_obj)
        return l_mqtt

    def SaveXml(self, p_xml):
        l_xml = mqttXML().write_mqtt_xml(self.m_pyhouse_obj.Computer.Mqtt.Brokers)
        p_xml.append(l_xml)
        LOG.info("Saved Mqtt XML.")
        return p_xml

# ## The following are public commands that may be called from everywhere

    def MqttPublish(self, p_topic, message_json = None, message_obj = None):
        """Send a topic, message to the broker for it to distribute to the subscription list

        self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish("schedule/execute", message-json = l_schedule_json)
        @param p_topic: is the partial topic, the prefix will be prepended.
        @param message_json : is the json message we want to send
        @param message_obj: is an additional object thhat we will convert to json and merge it into the message.
        """
        l_topic = Util._make_topic(self.m_pyhouse_obj, p_topic)
        l_message = Util._make_message(self.m_pyhouse_obj, message_json, message_obj)
        for l_broker in self.m_pyhouse_obj.Computer.Mqtt.Brokers.itervalues():
            if not l_broker.Active:
                continue
            try:
                l_broker._ProtocolAPI.publish(l_topic, l_message)
                LOG.info('Mqtt publishing:\n\tBroker: {}\n\tTopic:{}'.format(l_broker.Name, l_topic))
            except AttributeError as e_err:
                LOG.error("Mqtt Unpublished.\n\tERROR:{}\n\tTopic:{}\n\tMessage:{}".format(e_err, l_topic, l_message))

    def MqttDispatch(self, p_topic, p_message):
        """Dispatch a received MQTT message according to the topic.
        """
        l_topic = p_topic.split('/')[2:]  # Drop the pyhouse/housename/ as that is all we subscribed to.
        l_message = json_tools.decode_json_unicode(p_message)
        LOG.info('Dispatch\n\tTopic: {}'.format(l_topic))
        #
        if l_topic[0] == 'login':
            LOG.info('Login: {}'.format(PrettyFormatAny.form(l_message, 'Message', 80)))
        elif l_topic[0] == 'lighting':
            LOG.info('Lighting: {}'.format(PrettyFormatAny.form(l_message, 'Message', 80)))
        else:
            LOG.info('OTHER: {}'.format(PrettyFormatAny.form(l_message, 'Message', 80)))


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
        self.MqttPublish('login/initial', message_json = l_json)

# ## END DBK
