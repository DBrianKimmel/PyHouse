"""
-*- test-case-name: PyHouse.src.Modules.Computer.Nodes.test.XXtest_nodes -*-

@name:      PyHouse/src/Modules/Computer/Nodes/nodes.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 6, 2014
@summary:   This module does everything for nodes.

First, it uses node_local to gather the information about the node on which we are running.
Second, it uses node_discovery to find all the running nodes in the domain.
    Nodes may come and go within the domain.
Third, inter_node_comm is used to build up a model of all the nodes in a domain.
    It also tries to keep track of the active status of each node.
"""

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Computer.Nodes.node_local import API as localAPI
from Modules.Computer.Nodes.nodes_xml import Xml as nodesXml
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Nodes          ')


class API(object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_local = localAPI(p_pyhouse_obj)

    def LoadXml(self, p_pyhouse_obj):
        """ Load the Mqtt xml info.
        """
        l_nodes = nodesXml.read_all_nodes_xml(p_pyhouse_obj)
        p_pyhouse_obj.Computer.Nodes = l_nodes
        return l_nodes

    def Start(self):
        self.m_local.Start()
        #  self.m_discovery.Start()

    def SaveXml(self, p_xml):
        l_xml = nodesXml.write_nodes_xml(self.m_pyhouse_obj.Computer.Nodes)
        p_xml.append(l_xml)
        LOG.info("Saved XML.")
        return l_xml  # For testing

    def Stop(self):
        #  self.m_discovery.Stop()
        self.m_local.Stop()

#  ## END DBK
