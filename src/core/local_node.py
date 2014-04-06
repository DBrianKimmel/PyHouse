"""
@name: PyHouse/src/core/local_node.py

# -*- test-case-name: PyHouse.src.core.test.test_local_node -*-

Created on Apr 2, 2014

@author: briank

@copyright: 2014 by D. Brian Kimmel

@summary: Gather this nodes information.

This module:
    Gathers the information about this node and saves it in PyHousesData.
    Starts services on the local node (i.e. ir_service).
"""

# Import system type stuff
import logging
import netifaces
import os
import platform

# from src.core.nodes import NodeData
from src.communication import ir_control


g_debug = 0
g_logger = logging.getLogger('PyHouse.LocalNode   ')


NODE_NOTHING = 0x0000
NODE_LIGHTS = 0x0001
NODE_PANDORA = 0x0002
NODE_CAMERA = 0x0004
NODE_PIFACECAD = 0x0008
NODE_V6ROUTER = 0x0010


class InterfaceData(object):
    """
    Holds information about each of the interfaces on the local node.

    @param  Type: Ethernet | Wireless | Loop | Tunnel | Other
    """
    def __init__(self):
        self.Name = None
        self.Key = 0
        self.Active = True
        self.Type = None
        self.MacAddress = ''
        self.V4Address = []
        self.V6Address = []


class NodeRoleData(object):

    def __init__(self):
        self.CameraNode = False
        self.LightingNode = False
        self.PifaceCadNode = False
        self.PandoraNode = False


class NodeData(object):

    def __init__(self):
        self.Name = None
        self.Key = 0
        self.Active = True
        self.HostName = ''
        self.ConnectionAddr = None
        self.Role = 0
        self.Interfaces = {}


class GetNodeInfo(object):
    """Get the information about this node and stick it in NodeData
    """
    def __init__(self, p_node):
        p_node.Name = platform.node()


class GetAllInterfaceData(object):
    """Loop thru all the interfaces and extract the info
    """
    def __init__(self, p_node):
        """
        @type p_node: C{NodeData}
        @param p_node: the node information
        """
        l_interfaces = netifaces.interfaces()
        l_count = 0
        global InterfacesData
        for l_ix in l_interfaces:
            l_interface = InterfaceData()
            l_interface.Type = 'Other'
            l_interface.Name = l_ix
            l_interface.Key = l_count
            for l_af in netifaces.ifaddresses(l_ix):
                if netifaces.address_families[l_af] == 'AF_PACKET':
                    l_interface.MacAddress = self._get_list(netifaces.ifaddresses(l_ix)[l_af])
                if netifaces.address_families[l_af] == 'AF_INET':
                    l_interface.V4Address = self._get_list(netifaces.ifaddresses(l_ix)[l_af])
                if netifaces.address_families[l_af] == 'AF_INET6':
                    l_interface.V6Address = self._get_list(netifaces.ifaddresses(l_ix)[l_af])
            if l_interface.V4Address == [] and l_interface.V6Address == []:
                continue
            g_logger.info("Interface:{0:}, Mac:{1:}, V4:{2:}, V6:{3:} - {4:}".format(l_interface.Name, l_interface.MacAddress, l_interface.V4Address, l_interface.V6Address, l_count))
            p_node.Interfaces[l_count] = l_interface
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


class Utility(object):

    def insert_node(self, p_node, p_pyhouses_obj):
        """The local node should always be node 0 - Do I want to force it ???
        """
        l_max_key = -1
        try:
            for l_node in p_pyhouses_obj.CoreData.Nodes.itervalues():
                if l_node.Name == p_node.Name:
                    p_pyhouses_obj.CoreData.Nodes[l_node.Key] = p_node
                    return
                if l_node.Key > l_max_key:
                    l_max_key = l_node.Key
        except AttributeError:
            pass
        p_pyhouses_obj.CoreData.Nodes[l_max_key + 1] = p_node
        g_logger.debug('Nodes = {0:}'.format(p_pyhouses_obj.CoreData.Nodes))


class API(Utility):

    m_node = None

    def __init__(self):
        self.m_node = NodeData()
        GetNodeInfo(self.m_node)
        GetAllInterfaceData(self.m_node)
        self.m_node = HandleNodeType()

    def Start(self, p_pyhouses_obj):
        self.insert_node(self.m_node, p_pyhouses_obj)

    def Stop(self):
        pass

# ## END DBK
