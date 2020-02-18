"""
@name:       Modules/Computer/Nodes/node_sync.py
@author:     D. Brian Kimmel
@contact:    d.briankimmel@gmail.com
@copyright:  2016-2020 by D. Brian Kimmel
@date:       Created on Apr 27, 2016
@licencse:   MIT License
@summary:    Sync the nodes between all nodes.

"""

__updated__ = '2020-02-17'
__version_info__ = (20, 1, 25)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import datetime

#  Import PyMh files and modules.
from Modules.Computer.Nodes import NodeInformation
from Modules.Core.Utilities import extract_tools
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.NodeSync       ')

SECONDS = 1
MINUTES = 60 * SECONDS
HOURS = MINUTES * 60
INITIAL_DELAY = 15 * SECONDS
REPEAT_DELAY = 4 * HOURS


class NodeMessage():
    """
    """


class Utility:
    """
    """
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def send_who_is_there(self):
        l_topic = "computer/node/sync/whoisthere"
        l_uuid = self.m_pyhouse_obj.Computer.UUID
        try:
            l_node = self.m_pyhouse_obj.Computer.Nodes[l_uuid]
        except KeyError as e_err:
            LOG.error('No such node {}'.format(e_err))
            l_node = NodeInformation()
        l_node.NodeInterfaces = None
        self.m_pyhouse_obj.Core.MqttApi.MqttPublish(l_topic, l_node)

        # l_topic = 'computer/login/initial'
        # l_message = {}
        # p_pyhouse_obj.Core.MqttApi.MqttPublish(l_topic, l_message)

        self.m_pyhouse_obj._Twisted.Reactor.callLater(REPEAT_DELAY, self.send_who_is_there)

    def send_i_am(self):
        l_topic = "computer/node/sync/iam"
        l_uuid = self.m_pyhouse_obj.Computer.UUID
        l_node = self.m_pyhouse_obj.Computer.Nodes[l_uuid]
        self.m_pyhouse_obj.Core.MqttApi.MqttPublish(l_topic, l_node)

    def add_node(self, p_message_obj):
        """ Add node (or update if alreeady present).
        @param p_message_obj: is a decoded json message containing node information
        """
        return

        l_nodes = self.m_pyhouse_obj.Computer.Nodes
        l_uuid = p_message_obj['UUID']
        l_name = p_message_obj['Name']
        l_now = datetime.datetime.now()
        if l_uuid in l_nodes:
            LOG.info('Node already present {} '.format(l_name))
            self.m_pyhouse_obj.Computer.Nodes[l_uuid].LastUpdate = l_now
        else:
            LOG.info('Node not present - Adding. {}  {}'.format(l_uuid, l_name))
            l_obj = NodeInformation()
            l_obj.Name = l_name
            l_obj.Key = l_uuid
            # l_obj.Active = p_message_obj['Active']
            l_obj.Comment = p_message_obj['Comment']
            l_obj.ConnectionAddr_IPv4 = p_message_obj['ConnectionAddr_IPv4']
            l_obj.ConnectionAddr_IPv6 = p_message_obj['ConnectionAddr_IPv6']
            l_obj.ControllerCount = p_message_obj['ControllerCount']
            l_obj.ControllerTypes = p_message_obj['ControllerTypes']
            l_obj.NodeId = p_message_obj['NodeId']
            l_obj.NodeRole = p_message_obj['NodeRole']
            l_obj.LastUpdate = l_now
            l_obj.UUID = l_uuid
            self.m_pyhouse_obj.Computer.Nodes[l_uuid] = l_obj
        l_list = ''
        for l_node in self.m_pyhouse_obj.Computer.Nodes:
            l_list += l_node + '\n\t'
        pass
        LOG.info('Contains {} Nodes - {}'.format(len(self.m_pyhouse_obj.Computer.Nodes), l_list))


class Api:
    """
    """

    m_pyhouse_obj = None
    m_util = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_util = Utility(p_pyhouse_obj)
        LOG.info("Initialized - Version:{}".format(__version__))

    def _add_storage(self):
        """
        """

    def LoadConfig(self):
        pass

    def Start(self):
        LOG.info('Starting')
        self.m_runID = self.m_pyhouse_obj._Twisted.Reactor.callLater(INITIAL_DELAY, self.m_util.send_who_is_there)

    def SaveConfig(self):
        pass

    def Stop(self):
        LOG.info("Stopped.")

    def DecodeMqttMessage(self, p_msg):
        """ decode the /computer/node/ Mqtt message
        """
        l_topic = p_msg.UnprocessedTopic
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        l_name = extract_tools.get_mqtt_field(p_msg.Payload, 'Name')
        p_msg.LogMessage += '\tNodeSync:\n'
        if l_topic == 'whoisthere':
            p_msg.LogMessage += '\tName: {}  who is there'.format(l_name)
            p_msg.LogMessage += '\t {}\n'.format(PrettyFormatAny.form(p_msg.Payload, 'Light Control'))
            self.m_util.send_i_am()
        elif l_topic == 'iam':
            p_msg.LogMessage += '\tName {}  i am'.format(l_name)
            p_msg.LogMessage += '\t {}\n'.format(PrettyFormatAny.form(p_msg.Payload, 'Light Control'))
            self.m_util.add_node(p_msg)
        else:
            p_msg.LogMessage += '*** Unknown computer/node/??? Message type {}'.format(l_topic)

# ## END DBK
