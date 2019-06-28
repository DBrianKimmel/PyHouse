"""
@name:      PyHouse/Project/src/Modules/Computer/Mqtt/mqtt.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Apr 25, 2017
@license:   MIT License
@summary:   This is basically the MQTT API interface that is used by all of pyhouse.

"""

__updated__ = '2019-06-26'
__version_info__ = (19, 5, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import copy
import datetime
import platform

#  Import PyMh files and modules.
from Modules.Core.data_objects import NodeData
from Modules.Core.Utilities import json_tools, xml_tools
from Modules.Core.Utilities.extract_tools import get_required_mqtt_field
from Modules.Core.Utilities import config_tools
from Modules.Computer.Mqtt.mqtt_client import Util as mqttUtil
from Modules.Computer.Mqtt.mqtt_data import MqttInformation, MqttJson, MqttBrokerInformation
from Modules.Housing.house import MqttActions as houseMqtt

# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Mqtt           ')

CONFIG_FILE_NAME = 'mqtt.yaml'


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


class Yaml:
    """ Extract the config info from the config file "mqtt.yaml"
    """

    def _extract_broker(self, p_broker, p_api):
        """ Extract one broker information
        @return: MqttBrokerInformation if defined, else None
        """
        l_obj = MqttBrokerInformation()
        l_obj._ClientAPI = p_api
        try:
            l_broker = p_broker['Broker']
        except:
            LOG.warn('No Broker: in mqtt.yaml')
            return None
        for l_key, l_val in l_broker.items():
            setattr(l_obj, l_key, l_val)
        # LOG.debug(PrettyFormatAny.form(l_obj, 'Broker', 190))
        LOG.info('Loaded broker: {}'.format(l_obj.Name))
        return l_obj

    def _extract_brokers(self, p_node, p_api):
        """
        """
        # LOG.info('Loading Config, Extract Broker info - Version:{}'.format(__version__))
        l_brokers = {}
        l_count = 0
        if p_node.YamlPath == None:
            LOG.error('No Mqtt Yaml file found.')
            return
        try:
            l_config = p_node.Yaml['Mqtt']
        except:
            LOG.error('No Mqtt: in "mqtt.yaml" file!')
            return None
        for l_item in l_config:
            l_broker = self._extract_broker(l_item, p_api)
            if l_broker != None:
                l_brokers[l_count] = l_broker
                l_count += 1
        # LOG.debug(PrettyFormatAny.form(l_brokers, 'Brokers', 190))
        LOG.info('Loaded {} Mqtt Brokers.'.format(l_count))
        return l_brokers

    def LoadYamlConfig(self, p_pyhouse_obj, p_api):
        """ Read the Mqtt.Yaml file.
        """
        LOG.info('Reading config file "{}".'.format(CONFIG_FILE_NAME))
        l_yaml = config_tools.Yaml(p_pyhouse_obj).read_yaml(CONFIG_FILE_NAME)
        p_pyhouse_obj.Computer.Mqtt.Brokers = self._extract_brokers(l_yaml, p_api)

        l_computer = platform.node()

        p_pyhouse_obj.Computer.Mqtt.ClientID = 'PyH-Comp-' + l_computer
        p_pyhouse_obj.Computer.Mqtt.Prefix = 'pyhouse/' + p_pyhouse_obj._Parameters.Name  # we have not configured house at this point

        # p_pyhouse_obj._Config.YamlTree.Mqtt = l_yaml

        return p_pyhouse_obj.Computer  # for testing purposes

    def SaveYamlConfig(self, p_pyhouse_obj):
        """
        There is nothing in the config that can be altered during runtime
        so there is no need to write out the Yaml file to back it up.
        """


class API:
    """ This interfaces to all of PyHouse.
    """

    m_actions = None

    def __init__(self, p_pyhouse_obj, p_parent):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_parent = p_parent
        p_pyhouse_obj.Computer.Mqtt = MqttInformation()
        p_pyhouse_obj.Computer.Mqtt.Prefix = 'ReSeT'
        # p_pyhouse_obj.Computer.Mqtt.Brokers = []
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self):
        """ Load the Mqtt Config info.
        """
        LOG.info("Loading Config - Version:{}".format(__version__))
        Yaml().LoadYamlConfig(self.m_pyhouse_obj, self)

    def Start(self):
        """
        """
        LOG.info("Starting - Version:{}".format(__version__))

        if self.m_pyhouse_obj.Computer.Mqtt.Brokers != {}:
            l_count = mqttUtil().connect_to_all_brokers(self.m_pyhouse_obj)
            LOG.info("Mqtt {} broker Connection(s) Started.".format(l_count))
        else:
            LOG.info('No Mqtt brokers are started.')
        return

    def SaveXml(self, p_xml):
        """
        There is nothing in the config that can be altered during runtime
        so there is no need to write out the Yaml file to back it up.
        """
        return None

    def Stop(self):
        LOG.info("Stopped.")

# ## The following are public commands that may be called from everywhere

    def MqttPublish(self, p_topic, p_message):
        """ Send a topic, message to the broker for it to distribute to the subscription list

        All publish commands point to here.
        This routine will run thru the list of brokers and publish to each broker.

        # self.m_pyhouse_obj._APIs.Computer.MqttAPI.MqttPublish("house/schedule/execute", l_schedule)

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
                LOG.error("Mqtt NOT published.\n\tFor Broker: {}\n\tERROR:{}\n\tTopic:{}\n\tMessage:{}".format(
                    l_broker.Name, e_err, l_topic, l_message))
                # LOG.error("{}".format(PrettyFormatAny.form(l_broker, 'Client', 190)))

    def _decodeLWT(self, _p_topic_list, p_message):
        l_logmsg = '\tLast Will:\n'
        l_logmsg += p_message
        return l_logmsg

    def MqttDispatch(self, p_topic: str, p_message: object):
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
