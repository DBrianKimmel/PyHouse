"""
@name:      Modules/Core/Mqtt/mqtt.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Apr 25, 2017
@license:   MIT License
@summary:   This is basically the MQTT Api interface that is used by all of pyhouse.

"""

__updated__ = '2019-12-02'
__version_info__ = (19, 11, 26)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import copy
import datetime
import platform

#  Import PyMh files and modules.
from Modules.Core.Config.config_tools import Api as configApi
from Modules.Core.data_objects import NodeInformation
from Modules.Core.Utilities import json_tools, xml_tools
from Modules.Core.Utilities.extract_tools import get_required_mqtt_field
from Modules.Core.Mqtt.mqtt_client import Util as mqttUtil
from Modules.House.house import MqttActions as houseMqtt
from Modules.Computer.computer import MqttActions as computerMqtt
from Modules.Core.Mqtt.mqtt_information import MqttJson, MqttBrokerWillInformation, MqttBrokerInformation, MqttInformation

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Mqtt           ')

CONFIG_NAME = 'mqtt'
MAX_PROTOCOL_VERSION = 5  # this is the hignest protocol version this package can do


def _make_topic(p_pyhouse_obj, p_topic):
    l_topic = p_pyhouse_obj.Core.Mqtt.Prefix + p_topic
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


class LocalConfig:
    """ Extract the config info from the config file "mqtt.yaml"
    """

    m_config = None
    m_pyH = house_obj = None

    def __init__(self, p_pyhouse_obj):
        # LOG.debug('Initializing')
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def _extract_will_group(self, _p_config):
        """
        """
        l_obj = MqttBrokerWillInformation()
        _l_required = ['Topic', 'Message']
        _l_allowed = ['QoS', 'Retain']
        # self.m_config.Tools(self.m_pyhouse_obj).extract_fields(l_obj, p_config, l_required, l_allowed)
        return l_obj

    def _extract_one_broker(self, p_config, p_api):
        """ Extract one broker information
        @param p_config: is a single brokers yaml ordereddict.
        @param p_api: is the Api for ???
        @return: MqttBrokerInformation if defined, else None
        """
        l_obj = MqttBrokerInformation()
        l_obj.Version = MAX_PROTOCOL_VERSION
        # LOG.debug('Config: {}'.format(p_config))
        l_obj._ClientApi = p_api
        for l_key, l_value in p_config.items():
            if l_key == 'Access':
                l_obj.Access = self.m_config.extract_access_group(l_value)
                # l_obj.Access.Name = None
                # l_obj.Access.Password = None
            elif l_key == 'Host':
                l_obj.Host = self.m_config.extract_host_group(l_value)
            elif l_key == 'Will':
                l_obj.Will = self._extract_will_group(l_value)
            else:
                setattr(l_obj, l_key, l_value)
        # LOG.debug(PrettyFormatAny.form(l_obj, 'Broker'))
        LOG.info('Loaded broker: "{}"'.format(l_obj.Name))
        return l_obj

    def _extract_all_brokers(self, p_config, p_api):
        """
        """
        l_brokers = {}
        l_count = 0
        # LOG.debug('Config: {}'.format(p_config))
        for _l_key, l_value in enumerate(p_config['Brokers']):
            # LOG.debug('Config: {}'.format(l_value))
            l_broker = self._extract_one_broker(l_value, p_api)
            if l_broker != None:
                l_brokers[l_count] = l_broker
                l_count += 1
        # LOG.debug(PrettyFormatAny.form(l_brokers, 'Brokers'))
        LOG.info('Loaded {} Mqtt Brokers.'.format(l_count))
        return l_brokers

    def load_yaml_config(self, p_api):
        """ Read the mqtt.yaml file.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_pyhouse_obj.Core.Mqtt = MqttInformation()
        self.m_pyhouse_obj.Core.Mqtt.ClientID = 'PyH-Comp-' + platform.node()
        self.m_pyhouse_obj.Core.Mqtt.Prefix = 'pyhouse/' + self.m_pyhouse_obj._Parameters.Name + '/'  # we have not configured house at this point
        l_yaml = self.m_config.read_config(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Mqtt']
        except:
            LOG.warn('The config file does not start with "Mqtt:"')
            return None
        l_brokers = self.m_pyhouse_obj.Core.Mqtt.Brokers = self._extract_all_brokers(l_yaml, p_api)
        return l_brokers  # For testing purposes


class Api:
    """ This interfaces to all of PyHouse.
    """

    m_actions = None
    m_local_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        LOG.info('Intializing - Version:{}'.format(__version__))
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        # self.Core.MqttApi = self
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        self.m_parent = self
        LOG.info("Initialized")

    def _add_storage(self):
        # LOG.debug('Adding')
        setattr(self.m_pyhouse_obj.Core, 'MqttApi', self)  # Clear before loading

    def LoadConfig(self):
        """ Load the Mqtt Config info.
        """
        LOG.info("Loading Config - Version:{}".format(__version__))
        self.m_local_config.load_yaml_config(self)

    def Start(self):
        """
        """
        LOG.info("Starting - Version:{}".format(__version__))

        if self.m_pyhouse_obj.Core.Mqtt.Brokers != {}:
            l_count = mqttUtil().connect_to_all_brokers(self.m_pyhouse_obj)
            LOG.info("Mqtt {} broker Connection(s) Started.".format(l_count))
        else:
            LOG.info('No Mqtt brokers are started.')
        return

    def SaveConfig(self):
        """
        There is nothing in the config that can be altered during runtime
        so there is no need to write out the Yaml file to back it up.
        """
        return None

    def Stop(self):
        _x = PrettyFormatAny.form('', '')
        LOG.info("Stopped.")

# ## The following are public commands that may be called from everywhere

    def MqttPublish(self, p_topic, p_message):
        """ Send a topic, message to all the brokers for it to distribute to the subscription list

        All publish commands point to here.
        This routine will run thru the list of brokers and publish to each broker.

        # self.m_pyhouse_obj.Core.MqttApi.MqttPublish("house/schedule/execute", l_schedule)

        @param p_topic: is the partial topic, the prefix will be prepended.
        @param p_message : is the message we want to send
        """
        l_topic = _make_topic(self.m_pyhouse_obj, p_topic)
        l_message = _make_message(self.m_pyhouse_obj, p_message)
        for l_broker in self.m_pyhouse_obj.Core.Mqtt.Brokers.values():
            try:
                l_broker._ProtocolApi.publish(l_topic, l_message)
                # LOG.debug('Mqtt published:\tTopic:{}'.format(p_topic))
            except AttributeError as e_err:
                LOG.error("Mqtt NOT published.\n\tFor Broker: {}\n\tERROR:{}\n\tTopic:{}\n\tMessage:{}".format(
                    l_broker.Name, e_err, l_topic, l_message))
                # LOG.error("{}".format(PrettyFormatAny.form(l_broker, 'Client', 190)))

    def _decodeLWT(self, p_message):
        l_logmsg = '\tLast Will:\n'
        l_logmsg += p_message
        return l_logmsg

    def MqttDispatch(self, p_msg):
        """ Dispatch a received MQTT message according to the topic.

        --> pyhouse/<HouseName>/<Division>/topic03/topic04/...

        @param p_msg: MqttMessageInformation()
        @return: a message to send to the log detailing the Mqtt message received.
        @attention: Has many side affects
        """
        l_topic_list = p_msg.Topic.split('/')[2:]  # Drop the pyhouse/<housename>/ as that is all we subscribed to.
        # LOG.debug('Dispatch:\n\tTopic List: {}'.format(l_topic_list))
        p_msg.LogMessage = 'Dispatch\n\tTopic: {}'.format(l_topic_list)
        # Lwt can be from any device
        if l_topic_list[0] == 'lwt':
            p_msg.LogMessage += self._decodeLWT(p_msg.Payload)
            LOG.info(p_msg.LogMessage)
        else:
            # Every other topic will have the following field(s).
            l_sender = get_required_mqtt_field(p_msg.Payload, 'Sender')
            p_msg.LogMessage += '\n\tSender: {}\n'.format(l_sender)
        # Branch on the <division> portion of the topic
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        if l_topic_list[0] == 'computer':
            computerMqtt(self.m_pyhouse_obj).decode(p_msg)
        elif l_topic_list[0] == 'house':
            houseMqtt(self.m_pyhouse_obj).decode(p_msg)
        else:
            p_msg.LogMessage += '   OTHER: Unknown topic\n' + \
                        '\tTopic: {};\n'.format(l_topic_list[0]) + \
                        '\tMessage: {};\n'.format(p_msg.Payload)
            LOG.warn(p_msg.LogMessage)
        # LOG.info(p_msg.LogMessage)

    def doPyHouseLogin(self, p_client, p_pyhouse_obj):
        """ Login to PyHouse via MQTT
        """
        self.m_client = p_client
        l_name = p_pyhouse_obj.Computer.Name
        try:
            l_node = copy.deepcopy(p_pyhouse_obj.Computer.Nodes[l_name])
        except (KeyError, TypeError):
            l_node = NodeInformation()
        l_node.NodeInterfaces = {}

# ## END DBK
