"""
@name: PyHouse/src/core/nodes.py

# -*- test-case-name: PyHouse.src.core.test.test_nodes -*-

Created on Mar 6, 2014

@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License

@summary: This module does everything for nodes.

First, it uses node_local to gather the information about the node on which we are running.
Second, it uses node_discovery to find all the running nodes in the domain.  Nodes may come and go within the domain.
Third, node_domain is used to build up a model of all the nodes in a domain.  It also tries to keep track of
the active status of each node.

Using a Raspberry Pi as a node works fine for about any function, but I expect that it will run out
of capacity if too many services are attempted on one node.

Therefore, a cluster of nodes (a domain), each one running a small number of tasks will probably be the norm.

This design will then need a way for each node to discover all its neighbor nodes and establish a
communication network so we can pass information between nodes.

This module will establish a domain network and use Twisted's AMP protocol to pass messages around.
"""

# Import system type stuff

from src.core import node_local
from src.core import node_discovery
from src.core import node_domain
from src.utils import pyh_log

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.Nodes       ')

__all__ = ['NodeData',
           "API"]


class NodeData(object):

    def __init__(self):
        self.Name = None
        self.Key = 0
        self.Active = True
        self.ConnectionAddr = None
        self.Role = 0
        self.Interfaces = {}


class API(object):

    def __init__(self):
        self.m_local = node_local.API()
        self.m_discovery = node_discovery.API()
        self.m_domain = node_domain.API()
        # LOG.info("Initialized.")

    def Start(self, p_pyhouses_obj):
        p_pyhouses_obj.CoreData.Nodes = {}
        self.m_local.Start(p_pyhouses_obj)
        self.m_discovery.Start(p_pyhouses_obj)
        self.m_domain.Start(p_pyhouses_obj)
        # LOG.info("Started.")

    def Stop(self, p_xml):
        self.m_domain.Stop(p_xml)
        self.m_discovery.Stop(p_xml)
        self.m_local.Stop(p_xml)
        LOG.info("Stopped.")

# ## END DBK
