"""
@name:      PyHouse/Project/src/Modules/Computer/Mqtt/mqtt.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Apr 25, 2017
@license:   MIT License
@summary:   This is basically the MQTT API interface that is used by all of pyhouse.

"""
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

__updated__ = '2019-06-08'
__version_info__ = (19, 5, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import copy
import datetime

#  Import PyMh files and modules.
from Modules.Core.data_objects import NodeData
from Modules.Core.Utilities import json_tools, xml_tools
from Modules.Core.Utilities.extract_tools import get_required_mqtt_field

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Mqtt           ')

from Modules.Housing.house import MqttActions as houseMqtt
from Modules.Computer.Mqtt.mqtt_client import Util as mqttUtil
from Modules.Computer.Mqtt.mqtt_data import MqttInformation, MqttJson
from Modules.Computer.Mqtt.mqtt_xml import Xml as mqttXML


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
    return l_json


class API():
    """ This interfaces to all of PyHouse.
    """

    m_actions = None

    def __init__(self, p_pyhouse_obj, p_parent):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_parent = p_parent
        p_pyhouse_obj.Computer.Mqtt = MqttInformation()
        p_pyhouse_obj.Computer.Mqtt.Prefix = 'ReSeT'
        p_pyhouse_obj.Computer.Mqtt.Brokers = {}
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadXml(self, p_pyhouse_obj):
        """ Load the Mqtt xml info.
        """
        LOG.info("Loading XML - Version:{}".format(__version__))
        l_mqtt = mqttXML.read_mqtt_xml(p_pyhouse_obj, self)
        p_pyhouse_obj.Computer.Mqtt = l_mqtt
        LOG.info("Loaded {} Brokers".format(len(l_mqtt.Brokers)))
        if p_pyhouse_obj.Computer.Mqtt.Brokers != {}:
            l_count = mqttUtil().connect_to_all_brokers(p_pyhouse_obj)
            LOG.info("Mqtt {} broker Connection(s) Started.".format(l_count))
        else:
            LOG.info('No Mqtt brokers are configured.')
        LOG.info("Loaded XML - Version:{}".format(__version__))
        return l_mqtt

    def Start(self):
        """
        """
        LOG.info("Starting - Version:{}".format(__version__))
        # self.m_actions = actMqttActions(self.m_pyhouse_obj)

    def SaveXml(self, p_xml):
        l_xml = mqttXML().write_mqtt_xml(self.m_pyhouse_obj.Computer.Mqtt)
        p_xml.append(l_xml)
        LOG.info("Saved Mqtt XML.")
        return p_xml

    def Stop(self):
        LOG.info("Stopped.")

# ## The following are public commands that may be called from everywhere

    def MqttPublish(self, p_topic, p_message):
        """ Send a topic, message to the broker for it to distribute to the subscription list

        All publish commands point to here.
        This routine will run thru the list of brokers and publish to each broker.

        # self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish("house/schedule/execute", l_schedule)

        @param p_topic: is the partial topic, the prefix will be prepended.
        @param p_message : is the message we want to send
        """
        l_topic = _make_topic(self.m_pyhouse_obj, p_topic)
        l_message = _make_message(self.m_pyhouse_obj, p_message)
        for l_broker in self.m_pyhouse_obj.Computer.Mqtt.Brokers.values():
            if not l_broker.Active:
                continue
            try:
                l_broker._ProtocolAPI.publish(l_topic, l_message)
                # LOG.debug('Mqtt published:\tTopic:{}'.format(p_topic))
            except AttributeError as e_err:
                LOG.error("Mqtt NOT published.\n\tERROR:{}\n\tTopic:{}\n\tMessage:{}".format(e_err, l_topic, l_message))
                LOG.error("{}".format(PrettyFormatAny.form(l_broker, 'Client', 190)))

    def _decodeLWT(self, _p_topic_list, p_message):
        l_logmsg = '\tLast Will:\n'
        l_logmsg += p_message
        return l_logmsg

    def MqttDispatch(self, p_topic, p_message):
        """ Dispatch a received MQTT message according to the topic.

        Handle:
            computer
            house
            login
            lwt
        Everything else is an error!

        --> pyhouse/<HouseName>/<Division>/topic03/topic04/...

        @param p_topic: is a string of the topic 'pyhouse/<housename>/house/entertainment/pandora/control
        @param p_message: is the JSON encoded string with all the data of the message
        @return: a message to send to the log detailing the Mqtt message received.
        """
        l_topic_list = p_topic.split('/')[2:]  # Drop the pyhouse/<housename>/ as that is all we subscribed to.
        # LOG.debug('Dispatch:\n\tTopic List: {}'.format(l_topic_list))
        l_logmsg = 'Dispatch\n\tTopic: {}'.format(l_topic_list)
        # Lwt can be from any device
        if l_topic_list[0] == 'lwt':
            l_logmsg += self._decodeLWT(l_topic_list, p_message)
            LOG.info(l_logmsg)
        else:
            # Every other topic will have the following field(s).
            l_sender = get_required_mqtt_field(p_message, 'Sender')
            l_logmsg += '\n\tSender: {}\n'.format(l_sender)
        # Branch on the <division> portion of the topic
        if l_topic_list[0] == 'computer':
            l_logmsg += self.m_parent.DecodeMqtt(l_topic_list[1:], p_message)
        elif l_topic_list[0] == 'house':
            l_logmsg += houseMqtt(self.m_pyhouse_obj).decode(l_topic_list[1:], p_message)
        elif l_topic_list[0] == 'login':
            l_logmsg += houseMqtt(self.m_pyhouse_obj).decode(l_topic_list[1:], p_message)
        else:
            l_logmsg += '   OTHER: Unknown topic\n'
            l_logmsg += '\tTopic: {};\n'.format(l_topic_list[0])
            l_logmsg += '\tMessage: {};\n'.format(p_message)
            LOG.warn(l_logmsg)
        # LOG.info(l_logmsg)

    def doPyHouseLogin(self, p_client, p_pyhouse_obj):
        """ Login to PyHouse via MQTT
        """
        self.m_client = p_client
        l_name = p_pyhouse_obj.Computer.Name
        try:
            l_node = copy.deepcopy(p_pyhouse_obj.Computer.Nodes[l_name])
        except (KeyError, TypeError):
            l_node = NodeData()
        l_node.NodeInterfaces = {}

# ## END DBK
