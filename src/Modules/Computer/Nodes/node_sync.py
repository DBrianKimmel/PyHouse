"""
-*- test-case-name:  PyHouse.src.Modules.Computer.Nodes.test_node_sync  -*-

@name:       PyHouse/src/Modules/Computer/Nodes/node_sync.py
@author:     D. Brian Kimmel
@contact:    d.briankimmel@gmail.com
@copyright:  2016-2016 by D. Brian Kimmel
@date:       Created on Apr 27, 2016
@licencse:   MIT License
@summary:

"""

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.data_objects import NodeData
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.NodeSync       ')

INITIAL_DELAY = 15
REPEAT_DELAY = 60 * 60 * 4  # Every 4 hours


class Util(object):
    """
    """

    @staticmethod
    def send_whose_there(p_pyhouse_obj):
        l_topic = "computer/node/whosethere"
        l_uuid = p_pyhouse_obj.Computer.UUID
        try:
            l_node = p_pyhouse_obj.Computer.Nodes[l_uuid]
        except KeyError as e_err:
            LOG.error('No such node {}'.format(e_err))
            l_node = NodeData()
        p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, l_node)  # /lighting/{}/info
        _l_runID = p_pyhouse_obj.Twisted.Reactor.callLater(REPEAT_DELAY, Util.send_whose_there, p_pyhouse_obj)

    def send_i_am(self, p_pyhouse_obj):
        l_topic = "computer/node/iam"
        l_uuid = p_pyhouse_obj.Computer.UUID
        p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, p_pyhouse_obj.Computer.Nodes[l_uuid])  # /lighting/{}/info


class API(object):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def LoadXml(self, p_pyhouse_obj):
        pass

    def Start(self):
        LOG.info('Starting')
        self.m_runID = self.m_pyhouse_obj.Twisted.Reactor.callLater(INITIAL_DELAY, Util.send_whose_there, self.m_pyhouse_obj)
        pass

    def SaveXml(self, p_xml):
        pass

    def Stop(self):
        LOG.info("Stopped.")

    def DecodeMqttMessage(self, p_topic, p_message):
        l_msg = ' NodeSync '
        if p_topic[2] == 'whosethere':
            l_msg += ' {} '.format(p_message['Name'])
        elif p_topic[2] == 'iam':
            pass
        else:
            l_msg += 'Unknown Message type {}'.format(p_topic)
        return l_msg

# ## END DBK
