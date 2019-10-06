"""
@name:      Modules/Core/Mqtt/mqtt.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Apr 25, 2017
@license:   MIT License
@summary:   This is basically the MQTT Api interface that is used by all of pyhouse.

"""

__updated__ = '2019-10-06'
__version_info__ = (19, 10, 4)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import copy
import datetime
import platform

#  Import PyMh files and modules.
from Modules.Core.Config.config_tools import Api as configApi
from Modules.Core.data_objects import NodeInformation, HostInformation
from Modules.Core.Utilities import json_tools, xml_tools
from Modules.Core.Utilities.extract_tools import get_required_mqtt_field
from Modules.Core.Mqtt.mqtt_client import Util as mqttUtil
from Modules.House.house import MqttActions as houseMqtt
from Modules.Computer.computer import MqttActions as computerMqtt

# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Mqtt           ')

CONFIG_NAME = 'mqtt'


class MqttInformation:
    """

    ==> PyHouse.Core.Mqtt.xxx as in the def below
    """

    def __init__(self):
        self.Brokers = {}  # MqttBrokerData()
        self.ClientID = 'PyH-'
        self.Prefix = ''
        self._ClientAPI = None
        self._ProtocolAPI = None


class MqttBrokerInformation:
    """ 0-N

    ==> PyHouse.Core.Mqtt.Brokers.XXX as in the def below
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.Host = HostInformation()
        self.Class = 'Local'
        self.Keepalive = 60  # seconds
        self.Password = None
        self.UserName = None
        self.WillMessage = ''
        self.WillQoS = 0
        self.WillRetain = False
        self.WillTopic = ''

        self._ClientAPI = None
        self._ProtocolAPI = None
        self._isTLS = False


class MqttJson:
    """ This is a couple of pieces of information that get added into every MQTT message
        sent out of this computer.
    """

    def __init__(self):
        self.Sender = ''  # The Mqtt name of the sending device.
        self.DateTime = None  # The time on the sending device


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
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def _extract_one_broker(self, p_broker, p_api):
        """ Extract one broker information
        @param p_broker: is a single brokers yaml ordereddict.
        @param p_api: is the Api for ???
        @return: MqttBrokerInformation if defined, else None
        """
        l_obj = MqttBrokerInformation()
        l_obj._ClientAPI = p_api
        try:
            l_broker = p_broker['Broker']
        except:
            LOG.warn('No Broker: in mqtt.yaml')
            return None
        for l_key, l_value in l_broker.items():
            if l_key == 'Host':
                l_value = self.m_config.extract_host_group(l_value)
            setattr(l_obj, l_key, l_value)
        # LOG.debug(PrettyFormatAny.form(l_obj, 'Broker'))
        LOG.info('Loaded broker: {}'.format(l_obj.Name))
        return l_obj

    def _extract_all_brokers(self, p_yaml, p_api):
        """
        """
        # LOG.info('Loading Config, Extract Broker info - Version:{}'.format(__version__))
        l_brokers = {}
        l_count = 0
        try:
            l_config = p_yaml['Mqtt']
        except:
            LOG.error('No Mqtt: in "mqtt.yaml" file!')
            return None
        for l_item in l_config:
            l_broker = self._extract_one_broker(l_item, p_api)
            if l_broker != None:
                l_brokers[l_count] = l_broker
                l_count += 1
        # LOG.debug(PrettyFormatAny.form(l_brokers, 'Brokers', 190))
        LOG.info('Loaded {} Mqtt Brokers.'.format(l_count))
        return l_brokers

    def load_yaml_config(self, p_api):
        """ Read the Mqtt.Yaml file.
        """
        LOG.info('Reading mqtt config file "{}".'.format(CONFIG_NAME))
        l_node = self.m_config.read_config(CONFIG_NAME)
        if l_node == None:
            LOG.error('Missing {}'.format(CONFIG_NAME))
            return None
        l_yaml = l_node  # .Yaml
        l_obj = MqttInformation()
        l_obj.Brokers = self._extract_all_brokers(l_yaml, p_api)
        l_obj.ClientID = 'PyH-Comp-' + platform.node()
        l_obj.Prefix = 'pyhouse/' + self.m_pyhouse_obj._Parameters.Name + '/'  # we have not configured house at this point
        self.m_pyhouse_obj.Core.Mqtt = l_obj
        return l_obj  # for testing purposes


class Api:
    """ This interfaces to all of PyHouse.
    """

    m_actions = None
    m_local_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj, p_parent):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        self.m_parent = p_parent
        p_pyhouse_obj.Core.Mqtt = MqttInformation()
        p_pyhouse_obj.Core.Mqtt.Prefix = 'ReSeT'
        # p_pyhouse_obj.Core.Mqtt.Brokers = []
        LOG.info("Initialized - Version:{} == {}".format(__version__, self))

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
        LOG.info("Stopped.")

# ## The following are public commands that may be called from everywhere

    def MqttPublish(self, p_topic, p_message):
        """ Send a topic, message to the broker for it to distribute to the subscription list

        All publish commands point to here.
        This routine will run thru the list of brokers and publish to each broker.

        # self.m_pyhouse_obj._Apis.Core.MqttAPI.MqttPublish("house/schedule/execute", l_schedule)

        @param p_topic: is the partial topic, the prefix will be prepended.
        @param p_message : is the message we want to send
        """
        l_topic = _make_topic(self.m_pyhouse_obj, p_topic)
        l_message = _make_message(self.m_pyhouse_obj, p_message)
        for l_broker in self.m_pyhouse_obj.Core.Mqtt.Brokers.values():
            # if not l_broker.Active:
            #    continue
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
            l_logmsg += computerMqtt(self.m_pyhouse_obj).decode(l_topic_list[1:], p_message)
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
            l_node = NodeInformation()
        l_node.NodeInterfaces = {}

# ## END DBK
