#!/usr/bin/env python
"""
@name: PyHouse/src/core/setup.py

# -*- test-case-name: PyHouse.src.core.test.test_setup -*-

Created on Mar 1, 2014

@author: briank

@copyright: 2014 by D. Brian Kimmel

@summary: This will set up this node and then find all other nodes in the same cluster (House).

Then start the House and all the sub systems.
"""


# Import system type stuff
import logging
import os

from src.core import local_node
from src.core import nodes
from src.entertain import entertainment
from src.communication import ir_control


g_debug = 0
g_logger = logging.getLogger('PyHouse.CoreSetup   ')


INTER_NODE = 'tcp:port=8581'
INTRA_NODE = 'unix:path=/var/run/pyhouse/node:lockfile=1'

NODE_NOTHING = 0x0000
NODE_LIGHTS = 0x0001
NODE_PANDORA = 0x0002
NODE_CAMERA = 0x0004
NODE_PIFACECAD = 0x0008
NODE_V6ROUTER = 0x0010

InterfacesData = {}


class NodeRoleData(object):
    def __init__(self):
        self.CameraNode = False
        self.LightingNode = False
        self.PifaceCadNode = False
        self.PandoraNode = False


class HandleNodeType(object):

    m_node = NODE_NOTHING

    def __init__(self):
        self.find_node_type()

    def find_node_type(self):
        self.m_node = NODE_NOTHING
        # Test for lights
        if os.path.exists('/dev/ttyUSB0'):
            self.m_node |= NODE_LIGHTS
        # Test for Pandora
        if os.path.exists('/usr/bin/pianobar'):
            self.m_node |= NODE_PANDORA
        # Test for camera
        # Test for PifaceCAD
        if os.path.exists('/dev/lirc0'):
            self.m_node |= NODE_PIFACECAD

    def init_node_type(self, p_pyhouses_obj):
        if self.m_node & NODE_PIFACECAD:
            self._init_ir_control(p_pyhouses_obj)

    def _init_ir_control(self, p_pyhouses_obj):
        """This node has an IR receiver so set it up.
        """
        l_ir = ir_control.API()
        l_ir.Start(p_pyhouses_obj)


class API(object):

    m_entertainment = None
    m_node = None

    def __init__(self):
        g_logger.info("Initializing\n\n.")
        self.m_node = HandleNodeType()
        self.m_entertainment = entertainment.API()
        self.m_local_node = local_node.API()
        self.m_nodes = nodes.API()
        g_logger.info("Initialized.")

    def Start(self, p_pyhouses_obj):
        self.m_local_node.Start(p_pyhouses_obj)
        self.m_nodes.Start(p_pyhouses_obj)
        self.m_node.init_node_type(p_pyhouses_obj)
        # House
        # SubSystems
        self.m_entertainment.Start(p_pyhouses_obj)
        g_logger.info("Started.")

    def Stop(self, p_xml):
        # SubSystems
        self.m_entertainment.Stop(p_xml)
        # House
        g_logger.info("Stopped.")


if __name__ == "__main__":
    l_id = API()
    l_id.Start()

# ## END DBK
