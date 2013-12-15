"""
Created on Nov 23, 2013

@author: briank

This module is invoked by PyHouse.py.

It tries to figure out the which PyHouse on the local LAAN is the master.
It uses IPV6 to locate other PyHouse nodes.

Some nodes may be Camera/Security nodes.
Some nodes may be HVAC nodes
Some nodes may be Irrigation nodes.
Some nodes may control the various Entertainment systems
Some nodes may control various Pool/Spa devices.

"""

# Import system type stuff
import logging


g_debug = 0
g_logger = logging.getLogger('PyHouse.LocalMaster ')

class NodeRoleData(object):
    def __init__(self):
        self.CameraNode = False
        self.LightingNode = False


class FindNodeType(object):
    pass


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
