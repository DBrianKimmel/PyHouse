"""
@name: PyHouse/src/core/nodes.py

# -*- test-case-name: PyHouse.src.core.test.test_nodes -*-

Created on Mar 6, 2014

@author: briank

@copyright: 2014 by D. Brian Kimmel

@summary: This module does everything for nodes.

First, it uses local_node to gather the information about the node on which we are running.
Then, it uses node_discovery to find all the running nodes in the domain.  Nodes may come and go within the domain.
Last, node_proto is used to build up a model of all the nodes in a domain.  It also tries to keep track of
the active status of each node.

Using a Raspberry Pi as a node works fine for about any function, but I expect that it will run out
of capacity if too many services are attempted on one node.

Therefore, a cluster of nodes (a domain), each one running a small number of tasks will probably be the norm.

This design will then need a way for each node to discover all its neighbor nodes and establish a
communication network so we can pass information between nodes.

This module will establish a domain network and use Twisted's AMP protocol to pass messages around.
"""

# Import system type stuff
import logging

from src.core import local_node
from src.core import node_discovery
from src.core import node_proto


g_debug = 0
g_logger = logging.getLogger('PyHouse.Nodes       ')

class API(object):

    def __init__(self):
        self.m_local = local_node.API()
        self.m_discovery = node_discovery.API()
        self.m_domain = node_proto.API()
        g_logger.info("Initialized.")

    def Start(self, p_pyhouses_obj):
        p_pyhouses_obj.CoreData.Nodes = {}
        self.m_local.Start(p_pyhouses_obj)
        self.m_discovery.Start(p_pyhouses_obj)
        g_logger.info("Started.")

    def Stop(self):
        self.m_discovery.Stop()
        self.m_local.Stop()
        g_logger.info("Stopped.")

# ## END DBK
