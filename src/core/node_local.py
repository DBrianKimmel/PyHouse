"""
@name: PyHouse/src/core/node_local.py

# -*- test-case-name: PyHouse.src.core.test.test_node_local -*-

Created on Apr 2, 2014

@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License

@summary: Gather this node's information.

This module:
    Gathers information about the interfaces (ethernet, wifi etc.) on this node.
    Gathers information about the devices attached to this node.
    Gathers information about the specialized PyHouse software installed on this node.
    Saves all the gathered information in PyHousesData.
    Starts services on the local node (i.e. ir_service).

The discovered services may be fooled bu non PyHouse devices plugged into toe computer so it is possible to override the role
via configuration.  Once overridden the nwe role will "stick" by being written into the local XML file.
"""

# Import system type stuff
import fnmatch
import logging
import netifaces
import os
import platform

from src.communication import ir_control

g_debug = 0
g_logger = logging.getLogger('PyHouse.NodeLocal   ')


__all__ = ['NODE_NOTHING', 'NODE_LIGHTS',
           'NODE_PANDORA', 'NODE_CAMERA',
           'NODE_PIFACECAD', 'NODE_V6ROUTER',
           'API'
           ]


NODE_NOTHING = 0x0000
NODE_LIGHTS = 0x0001
NODE_PANDORA = 0x0002
NODE_CAMERA = 0x0004
NODE_PIFACECAD = 0x0008
NODE_V6ROUTER = 0x0010
NODE_WINDOWS = 0x0020
NODE_TUNNEL = 0x0040


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


class NodeData(object):

    def __init__(self):
        self.Name = None
        self.Key = 0
        self.Active = True
        self.ConnectionAddr = None
        self.Role = 0
        self.Interfaces = {}


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

    def __init__(self, p_role):
        self.find_node_type(p_role)

    def init_node_type(self, p_pyhouses_obj):
        if self.m_node & NODE_PIFACECAD:
            self._init_ir_control(p_pyhouses_obj)


    def _init_ir_control(self, p_pyhouses_obj):
        """This node has an IR receiver so set it up.
        """
        l_ir = ir_control.API()
        l_ir.Start(p_pyhouses_obj)


class Utility(object):

    def get_node_info(self, p_pyhouses_obj):
        p_pyhouses_obj.CoreData.Nodes[0].Name = platform.node()
        p_pyhouses_obj.CoreData.Nodes[0].Key = 0
        p_pyhouses_obj.CoreData.Nodes[0].Active = True

    def find_node_role(self):
        p_role = NODE_NOTHING
        try:
            for l_file in os.listdir('/dev'):
                # Test for lights
                if fnmatch.fnmatch(l_file, 'ttyUSB?'):
                    p_role |= NODE_LIGHTS
                    g_logger.debug('Lighting Node')
                if fnmatch.fnmatch(l_file, 'lirc?'):
                    p_role |= NODE_PIFACECAD
                    g_logger.debug('Lirc Node')
            # Test for Pandora
            if os.path.exists('/usr/bin/pianobar'):
                p_role |= NODE_PANDORA
                g_logger.debug('Pandora Node')
            # Test for camera
            #
        except WindowsError:
            p_role |= NODE_WINDOWS
            g_logger.debug('Windows Node')
        return p_role

    def init_node_type(self, p_pyhouses_obj):
        l_role = p_pyhouses_obj.CoreData.Nodes[0].Role
        if l_role & NODE_PIFACECAD:
            self._init_ir_control(p_pyhouses_obj)
        elif l_role & NODE_LIGHTS:
            pass
        elif l_role & NODE_CAMERA:
            pass

    def _init_ir_control(self, p_pyhouses_obj):
        """This node has an IR receiver so set it up.
        """
        l_ir = ir_control.API()
        l_ir.Start(p_pyhouses_obj)

    def insert_node(self, p_node, p_pyhouses_obj):
        return
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
        pass

    def Start(self, p_pyhouses_obj):
        self.m_node = NodeData()
        GetAllInterfaceData(self.m_node)
        p_pyhouses_obj.CoreData.Nodes[0] = self.m_node
        self.get_node_info(p_pyhouses_obj)
        p_pyhouses_obj.CoreData.Nodes[0].Role = self.find_node_role()
        self.init_node_type(p_pyhouses_obj)
        g_logger.info('Started')

    def Stop(self):
        pass

# ## END DBK
