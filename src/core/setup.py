#!/usr/bin/env python
"""
setup.py

Created on Mar 1, 2014

@author: briank

@copyright: 2014 by D. Brian Kimmel

@summary: This will set up this node and then find all other nodes in the same cluster (House).

Then start the House and all the sub systems.
"""


# Import system type stuff
import logging
import netifaces
import os
import platform

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


class NodeData(object):
    def __init__(self):
        self.Name = None
        self.Key = 0
        self.Active = True
        self.HostName = ''
        self.Role = None
        self.Interfaces = []

class InterfaceData(object):
    def __init__(self):
        self.Name = None
        self.Key = 0
        self.Active = True
        self.MacAddress = ''
        self.V4Address = []
        self.V6Address = []


class NodeRoleData(object):
    def __init__(self):
        self.CameraNode = False
        self.LightingNode = False
        self.PifaceCadNode = False
        self.PandoraNode = False


class FindAllInterfaceData(object):
    """Loop thru all the interfaces and extract the info
    """
    def __init__(self):
        l_interfaces = netifaces.interfaces()
        if g_debug >= 1:
            g_logger.debug(l_interfaces)
        l_count = 0
        global InterfacesData
        for l_interface in l_interfaces:
            if l_interface == 'lo':
                continue
            m_interface = InterfaceData()
            m_interface.Name = l_interface
            m_interface.Key = l_count
            for l_af in netifaces.ifaddresses(l_interface):
                if g_debug >= 1:
                    g_logger.debug(l_af)
                if netifaces.address_families[l_af] == 'AF_PACKET':
                    m_interface.MacAddress = self._get_list(netifaces.ifaddresses(l_interface)[l_af])
                if netifaces.address_families[l_af] == 'AF_INET':
                    m_interface.V4Address = self._get_list(netifaces.ifaddresses(l_interface)[l_af])
                if netifaces.address_families[l_af] == 'AF_INET6':
                    if g_debug >= 1:
                        g_logger.debug(netifaces.ifaddresses(l_interface)[l_af])
                    m_interface.V6Address = self._get_list(netifaces.ifaddresses(l_interface)[l_af])
            g_logger.info("Interface:{0}, Mac:{1:}, V4:{2:}, V6:{3:}".format(m_interface.Name, m_interface.MacAddress, m_interface.V4Address, m_interface.V6Address))
            InterfacesData[l_count] = m_interface
            l_count += 1

    def _get_list(self, p_list):
        l_list = []
        for l_ent in p_list:
            l_list.append(l_ent['addr'])
        return l_list


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


class FindRouter(object):
    pass


class LocateLocalNodes(object):
    """Find nodes in this house
    """
    def __init__(self):
        pass


class GetNodeInfo(object):
    """Get the information about this node and stick it in NodeData
    """
    def __init__(self):
        NodeData.Name = platform.node()


class API(object):

    m_entertainment = None
    m_node = None

    def __init__(self):
        self.m_node = HandleNodeType()
        self.m_entertainment = entertainment.API()
        FindAllInterfaceData()
        LocateLocalNodes()
        self.m_nodes = nodes.API()
        g_logger.info("Initialized.")

    def Start(self, p_pyhouses_obj):
        p_pyhouses_obj.Nodes = InterfacesData
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

    def _UpdateXml (self, p_xml):
        pass

if __name__ == "__main__":
    l_id = API()
    l_id.Start()

# ## END DBK
