"""
-*- test-case-name:  PyHouse.src.Modules.Computer.Nodes.test_nodes_sync  -*-

@name:       PyHouse/src/Modules/Computer/Nodes/nodes_sync.py
@author:     D. Brian Kimmel
@contact:    d.briankimmel@gmail.com
@copyright:  2016-2016 by D. Brian Kimmel
@date:       Created on Apr 27, 2016
@licencse:   MIT License
@summary:

"""

#  Import system type stuff

#  Import PyMh files and modules.
# from Modules.Core.data_objects import NodeData
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.NodeSync       ')


class Util(object):
    """
    """

    def send_whose_there(self, p_pyhouse_obj):
        l_topic = "computer/node/whosethere"
        l_uuid = p_pyhouse_obj.Computer.UUID
        p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, p_pyhouse_obj.Computer.Node[l_uuid])  # /lighting/{}/info

    def send_i_am(self, p_pyhouse_obj):
        l_topic = "computer/node/iam"
        l_uuid = p_pyhouse_obj.Computer.UUID
        p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, p_pyhouse_obj.Computer.Node[l_uuid])  # /lighting/{}/info


class API(object):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def LoadXml(self, p_pyhouse_obj):
        pass

    def Start(self):
        pass

    def SaveXml(self, p_xml):
        pass

    def Stop(self):
        LOG.info("Stopped.")


# ## END DBK
