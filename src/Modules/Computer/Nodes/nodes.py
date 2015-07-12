"""
-*- test-case-name: PyHouse.src.Modules.Computer.Nodes.test.test_nodes -*-

@name:      PyHouse/src/Modules/Computer/Nodes/nodes.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 6, 2014
@summary:   This module does everything for nodes.

First, it uses node_local to gather the information about the node on which we are running.
Second, it uses node_discovery to find all the running nodes in the domain.
    Nodes may come and go within the domain.
Third, inter_node_comm is used to build up a model of all the nodes in a domain.
    It also tries to keep track of the active status of each node.

Using a Raspberry Pi as a node works fine for about any function, but I expect that it will run out
of capacity if too many services are attempted on one node.

Therefore, a cluster of nodes (a domain), each one running a small number of tasks will probably be the norm.

This design will then need a way for each node to discover all its neighbor nodes and establish a
communication network so we can pass information between nodes.

This module will establish a domain network and use Twisted's AMP protocol to pass messages around.

"""

# Import system type stuff

# Import PyMh files and modules.
from Modules.Computer.Nodes.node_discovery import API as discoveryAPI
from Modules.Computer.Nodes.node_local import API as localAPI

g_debug = 0


class API(object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_local = localAPI(p_pyhouse_obj)
        self.m_discovery = discoveryAPI(p_pyhouse_obj)

    def Start(self):
        self.m_local.Start()
        self.m_discovery.Start()

    def Stop(self):
        self.m_discovery.Stop()
        self.m_local.Stop()

    def SaveXml(self, p_xml):
        self.m_discovery.SaveXml(p_xml)
        self.m_local.SaveXml(p_xml)
        return p_xml

# ## END DBK
