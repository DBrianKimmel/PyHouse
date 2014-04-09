"""
@name: PyHouse/src/core/setup.py

# -*- test-case-name: PyHouse.src.core.test.test_setup -*-

Created on Mar 1, 2014

@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License

@summary: This module sets up the core part of PyHouse.

This will set up this node and then find all other nodes in the same domain (House).

Then start the House and all the sub systems.
"""

# Import system type stuff
import logging

from src.core import nodes
from src.entertain import entertainment

g_debug = 0
g_logger = logging.getLogger('PyHouse.CoreSetup   ')

INTER_NODE = 'tcp:port=8581'
INTRA_NODE = 'unix:path=/var/run/pyhouse/node:lockfile=1'


class CoreData(object):

    def __init__(self):
        self.Nodes = {}
        self.DiscoveryService = None
        self.DomainService = None


class API(object):

    m_entertainment = None
    m_node = None

    def __init__(self):
        g_logger.info("\n-----------------------------\nInitializing\n\n")
        self.m_nodes = nodes.API()
        self.m_entertainment = entertainment.API()
        g_logger.info("Initialized.\n\n")

    def Start(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj
        p_pyhouses_obj.CoreData = CoreData()
        self.m_nodes.Start(p_pyhouses_obj)
        # House
        # SubSystems
        self.m_entertainment.Start(p_pyhouses_obj)
        g_logger.info("Started.")

    def Stop(self, p_xml):
        # SubSystems
        self.m_entertainment.Stop(p_xml)
        # House
        self.m_nodes.Stop(p_xml)
        g_logger.info("Stopped.")

# ## END DBK
