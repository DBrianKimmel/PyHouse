#!/usr/bin/env python
"""
@name: PyHouse/src/core/setup.py

# -*- test-case-name: PyHouse.src.core.test.test_setup -*-

Created on Mar 1, 2014

@author: briank

@copyright: 2014 by D. Brian Kimmel

@summary: This module sets up the core part of PyHouse.

This will set up this node and then find all other nodes in the same domain (House).

Then start the House and all the sub systems.
"""


# Import system type stuff
import logging
import os

from src.core import nodes
from src.entertain import entertainment
from src.communication import ir_control


g_debug = 0
g_logger = logging.getLogger('PyHouse.CoreSetup   ')


INTER_NODE = 'tcp:port=8581'
INTRA_NODE = 'unix:path=/var/run/pyhouse/node:lockfile=1'

InterfacesData = {}


class CoreData(object):

    def __init__(self):
        self.Nodes = {}


class HandleNodeType(object):

    def _init_ir_control(self, p_pyhouses_obj):
        """This node has an IR receiver so set it up.
        """
        l_ir = ir_control.API()
        l_ir.Start(p_pyhouses_obj)


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


if __name__ == "__main__":
    l_id = API()
    l_id.Start()

# ## END DBK
