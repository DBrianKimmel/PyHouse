"""
Created on Nov 23, 2013

@author: briank

This module is invoked by PyHouse.py.

It tries to figure out the which PyHouse on the local LAN is the master.
It uses IPV6 to locate other PyHouse nodes.

Some nodes may be Camera/Security nodes.
Some nodes may be HVAC nodes
Some nodes may be Irrigation nodes.
Some nodes may control the various Entertainment systems
Some nodes may control various Pool/Spa devices.

There is a port, 18580, that is used for inter-node communication.

"""
NODE_NOTHING = 0x0000
NODE_LIGHTS = 0x0001
NODE_PANDORA = 0x0002
NODE_CAMERA = 0x0004
NODE_PIFACECAD = 0x0008
NODE_V6ROUTER = 0x0010

# Import system type stuff
import logging
import os


g_debug = 0
g_logger = logging.getLogger('PyHouse.LocalMaster ')

class NodeRoleData(object):
    def __init__(self):
        self.CameraNode = False
        self.LightingNode = False


class FindNodeTypes(object):

    def __init__(self):
        l_node = NODE_NOTHING
        # Test for lights
        if os.path.exists('/dev/ttyUSB0'):
            l_node |= NODE_LIGHTS
        # Test for Pandora
        # Test for camera
        # Test for PifaceCAD
        if os.path.exists('/dev/lirc0'):
            l_node |= NODE_PIFACECAD


class FindRouter(object):
    pass


class API(object):
    def __init__(self):
        pass

    def Start(self, p_pyhouses_obj):
        pass

    def Stop(self):
        pass

# ## END DBK
