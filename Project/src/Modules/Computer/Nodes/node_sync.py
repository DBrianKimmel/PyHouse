"""
-*- test-case-name:  PyHouse.src.Modules.Computer.Nodes.test_node_sync  -*-

@name:       PyHouse/src/Modules/Computer/Nodes/node_sync.py
@author:     D. Brian Kimmel
@contact:    d.briankimmel@gmail.com
@copyright:  2016-2019 by D. Brian Kimmel
@date:       Created on Apr 27, 2016
@licencse:   MIT License
@summary:    Sync the nodes between all nodes.

"""

__updated__ = '2019-01-19'

#  Import system type stuff
import datetime

#  Import PyMh files and modules.
from Modules.Core.data_objects import NodeData
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.NodeSync       ')

SECONDS = 1
MINUTES = 60 * SECONDS
HOURS = MINUTES * 60
INITIAL_DELAY = 15 * SECONDS
REPEAT_DELAY = 4 * HOURS


class NodeMessage():
    """
    """


class Util(object):
    """
    """

    @staticmethod
    def send_who_is_there(p_pyhouse_obj):
        l_topic = "computer/node/whoisthere"
        l_uuid = p_pyhouse_obj.Computer.UUID
        try:
            l_node = p_pyhouse_obj.Computer.Nodes[l_uuid]
        except KeyError as e_err:
            LOG.error('No such node {}'.format(e_err))
            l_node = NodeData()
        l_node.NodeInterfaces = None
        p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, l_node)  # /computer/node/whoisthere

        l_topic = 'login/initial'
        l_message = {}
        p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, l_message)  # /login/initial

        _l_runID = p_pyhouse_obj.Twisted.Reactor.callLater(REPEAT_DELAY, Util.send_who_is_there, p_pyhouse_obj)

    @staticmethod
    def send_i_am(p_pyhouse_obj):
        l_topic = "computer/node/iam"
        l_uuid = p_pyhouse_obj.Computer.UUID
        l_node = p_pyhouse_obj.Computer.Nodes[l_uuid]
        p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, l_node)  # /computer/node/iam

    @staticmethod
    def add_node(p_pyhouse_obj, p_message_obj):
        """ Add node (or update if alreeady present).
        @param p_message_obj: is a decoded json message containing node information
        """
        l_nodes = p_pyhouse_obj.Computer.Nodes
        l_uuid = p_message_obj['UUID']
        l_name = p_message_obj['Name']
        l_now = datetime.datetime.now()
        if l_uuid in l_nodes:
            LOG.info('Node already present {} '.format(l_name))
            p_pyhouse_obj.Computer.Nodes[l_uuid].LastUpdate = l_now
        else:
            LOG.info('Node not present - Adding. {}  {}'.format(l_uuid, l_name))
            l_obj = NodeData()
            l_obj.Name = l_name
            l_obj.Key = l_uuid
            l_obj.Active = p_message_obj['Active']
            l_obj.Comment = p_message_obj['Comment']
            l_obj.ConnectionAddr_IPv4 = p_message_obj['ConnectionAddr_IPv4']
            l_obj.ConnectionAddr_IPv6 = p_message_obj['ConnectionAddr_IPv6']
            l_obj.ControllerCount = p_message_obj['ControllerCount']
            l_obj.ControllerTypes = p_message_obj['ControllerTypes']
            l_obj.NodeId = p_message_obj['NodeId']
            l_obj.NodeRole = p_message_obj['NodeRole']
            l_obj.LastUpdate = l_now
            l_obj.UUID = l_uuid
            p_pyhouse_obj.Computer.Nodes[l_uuid] = l_obj
        l_list = ''
        for l_node in p_pyhouse_obj.Computer.Nodes:
            l_list += l_node + '\n\t'
        pass
        LOG.info('Contains {} Nodes - {}'.format(len(p_pyhouse_obj.Computer.Nodes), l_list))


class API(object):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def LoadXml(self, _p_pyhouse_obj):
        LOG.info("Initialized.")
        pass

    def Start(self):
        LOG.info('Starting')
        self.m_runID = self.m_pyhouse_obj.Twisted.Reactor.callLater(
                        INITIAL_DELAY, Util.send_who_is_there, self.m_pyhouse_obj)

    def SaveXml(self, p_xml):
        pass

    def Stop(self):
        LOG.info("Stopped.")

    def DecodeMqttMessage(self, p_topic, p_message):
        """ decode the /computer/node/ Mqtt message
        """
        l_msg = '\tNodeSync\n'
        if p_topic[2] == 'whoisthere':
            l_msg += '\tName: {}  who is there'.format(p_message['Name'])
            l_msg += '\t {}\n'.format(p_message)
            Util.send_i_am(self.m_pyhouse_obj)
        elif p_topic[2] == 'iam':
            l_msg += '\tName {}  i am'.format(p_message['Name'])
            l_msg += '\t {}\n'.format(p_message)
            Util.add_node(self.m_pyhouse_obj, p_message)
        else:
            l_msg += '*** Unknown computer/node/??? Message type {}'.format(p_topic[2])
        return l_msg

# ## END DBK
