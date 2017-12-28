"""
-*- test-case-name: /home/briank/workspace/PyHouse/src/Modules/Computer/Mqtt/mqtt.py -*-

@name:      /home/briank/workspace/PyHouse/src/Modules/Computer/Mqtt/mqtt.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@note:      Created on Apr 25, 2017
@license:   MIT License
@summary:   This is basically the MQTT API interface that is used by all of pyhouse.

"""

__updated__ = '2017-12-28'

#  Import system type stuff
import copy
import datetime

#  Import PyMh files and modules.
from Modules.Core.data_objects import MqttInformation, MqttJson, NodeData
from Modules.Core.Utilities import json_tools, xml_tools
from Modules.Computer.Mqtt.mqtt_actions import Actions
from Modules.Computer.Mqtt.mqtt_client import Util as mqttUtil
from Modules.Computer.Mqtt.mqtt_xml import Xml as mqttXML
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Mqtt           ')
from Modules.Core.Utilities.debug_tools import FormatBytes


def _make_topic(p_pyhouse_obj, p_topic):
    l_topic = p_pyhouse_obj.Computer.Mqtt.Prefix + p_topic
    return l_topic


def _make_message(p_pyhouse_obj, p_message=None):
    """
    @param p_pyhouse_obj: is the entire PyHouse Data tree.
    @param message_json: is message that is already json encoded\
    @param message_obj: is additional object that will be added into the meddage as Json.
    """
    l_message = MqttJson()
    l_message.Sender = p_pyhouse_obj.Computer.Name
    l_message.DateTime = datetime.datetime.now()
    if p_message is None:
        pass
    elif isinstance(p_message, object):
        xml_tools.stuff_new_attrs(l_message, p_message)
    else:
        xml_tools.stuff_new_attrs(l_message, p_message)
    l_json = json_tools.encode_json(l_message)
    # LOG.debug('Message:{}<<'.format(FormatBytes(l_json)))
    return l_json


class API(object):
    """This interfaces to all of PyHouse.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.APIs.Computer.MqttAPI = self
        p_pyhouse_obj.Computer.Mqtt = MqttInformation()
        p_pyhouse_obj.Computer.Mqtt.Prefix = 'ReSeT'
        p_pyhouse_obj.Computer.Mqtt.Brokers = {}
        LOG.info("Initialized.")

    def LoadXml(self, p_pyhouse_obj):
        """ Load the Mqtt xml info.
        """
        LOG.info("Loading XML")
        l_mqtt = MqttInformation()
        l_mqtt.Prefix = p_pyhouse_obj.Computer.Name
        l_mqtt.Brokers = mqttXML.read_mqtt_xml(p_pyhouse_obj, self)
        p_pyhouse_obj.Computer.Mqtt = l_mqtt
        LOG.info("Loaded {} Brokers".format(len(l_mqtt.Brokers)))
        if p_pyhouse_obj.Computer.Mqtt.Brokers != {}:
            #  LOG.info('Connecting to all MQTT Brokers.')
            l_count = mqttUtil().connect_to_all_brokers(p_pyhouse_obj)
            LOG.info("Mqtt {} broker(s) Started.".format(l_count))
        else:
            LOG.info('No Mqtt brokers are configured.')
        LOG.info("Loaded XML")
        return l_mqtt

    def Start(self):
        """
        if self.m_pyhouse_obj.Computer.Mqtt.Brokers != {}:
            LOG.info('Connecting to all MQTT Brokers.')
            l_count = self.connect_to_all_brokers(self.m_pyhouse_obj)
            LOG.info("Mqtt {} broker(s) Started.".format(l_count))
        else:
            LOG.info('No Mqtt brokers are configured.')
        """
        pass

    def SaveXml(self, p_xml):
        l_xml = mqttXML().write_mqtt_xml(self.m_pyhouse_obj.Computer.Mqtt.Brokers)
        p_xml.append(l_xml)
        # LOG.info("Saved Mqtt XML.")
        return p_xml

    def Stop(self):
        LOG.info("Stopped.")

# ## The following are public commands that may be called from everywhere

    def MqttPublish(self, p_topic, p_message):
        """Send a topic, message to the broker for it to distribute to the subscription list

        # self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish("schedule/execute", l_schedule)
        @param p_topic: is the partial topic, the prefix will be prepended.
        @param message_json : is the JSON message we want to send
        @param message_obj: is an additional object that we will convert to JSON and merge it into the message.
        """
        l_topic = _make_topic(self.m_pyhouse_obj, p_topic)
        l_message = _make_message(self.m_pyhouse_obj, p_message)
        for l_broker in self.m_pyhouse_obj.Computer.Mqtt.Brokers.values():
            if not l_broker.Active:
                continue
            try:
                l_broker._ProtocolAPI.publish(l_topic, l_message)
                LOG.info('Mqtt published:\tTopic:{}'.format(p_topic))
            except AttributeError as e_err:
                LOG.error("Mqtt NOT published.\n\tERROR:{}\n\tTopic:{}\n\tMessage:{}".format(e_err, l_topic, l_message))

    def MqttDispatch(self, p_topic, p_message):
        """Dispatch a received MQTT message according to the topic.

        TODO: This needs protection from poorly formed Mqtt messages.
        """
        l_topic = p_topic.split('/')[2:]  # Drop the pyhouse/housename/ as that is all we subscribed to.
        # l_message = json_tools.decode_json_unicode(p_message)
        l_message = p_message
        l_logmsg = Actions(self.m_pyhouse_obj).mqtt_dispatch(l_topic, l_message)
        LOG.info(l_logmsg)

    def doPyHouseLogin(self, p_client, p_pyhouse_obj):
        """Login to PyHouse via MQTT
        """
        self.m_client = p_client
        l_name = p_pyhouse_obj.Computer.Name
        try:
            l_node = copy.deepcopy(p_pyhouse_obj.Computer.Nodes[l_name])
        except (KeyError, TypeError):
            l_node = NodeData()
        l_node.NodeInterfaces = {}

# ## END DBK
