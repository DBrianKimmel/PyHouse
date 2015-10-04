"""
-*- test-case-name: PyHouse.src.Modules.Comouter.Nodes.test.test_node_local -*-

@name:      PyHouse/src/Modules/Computer/Nodes/node_local.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015  by D. Brian Kimmel
@note:      Created on Apr 2, 2014
@license:   MIT License
@summary:   Gather this node's information.

This module:
    Gathers information about the interfaces (ethernet, wifi etc.) on this node.
    Gathers information about the controller devices attached to this node.
    Gathers information about the specialized PyHouse software installed on this node.
    Saves all the gathered information in p_pyhouse_obj.
    Starts services on the local node (i.e. ir_service).

The discovered services may be fooled by non PyHouse devices plugged into the computer
  so it will be possible to override the role via configuration.
Once overridden the new role will "stick" by being written into the local XML file.
"""

# Import system type stuff
import fnmatch  # Filename matching with shell patterns
import netifaces
import os
import platform

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData, NodeInterfaceData
from Modules.Communication import ir_control
from Modules.Computer import logging_pyh as Logger
# from Modules.Computer.Nodes import nodes_xml
from Modules.Utilities.debug_tools import PrettyFormatAny

LOG = Logger.getLogger('PyHouse.NodeLocal      ')


__all__ = ['NODE_NOTHING', 'NODE_LIGHTS',
           'NODE_PANDORA', 'NODE_CAMERA',
           'NODE_PIFACECAD', 'NODE_V6ROUTER',
           'API'
           ]


NODE_NOTHING = 0x0000  # a basic node with no special functions
NODE_LIGHTS = 0x0001  # Node has an attached controller for Lights (optionally other stuff)
NODE_PANDORA = 0x0002  # Node can use pianobar to receive Pandora streams
NODE_CAMERA = 0x0004  # Pi with attached camera (not USB camera)
NODE_PIFACECAD = 0x0008  #
NODE_V6ROUTER = 0x0010  # Iv6 Router node
NODE_WINDOWS = 0x0020  # Windowd - not Linux
NODE_TUNNEL = 0x0040  # IPv6 Tunnel
NODE_IR = 0x0080  # Infra-red receiver and optional transmitter


class Interfaces(object):
    """
    Loop thru all the interfaces and extract the info.
    """

    @staticmethod
    def find_all_interface_names():
        """
        Get the names of all the network interfaces on this computer.
        Windows return an UUID as the name
        Linux before about 2015 returned something like eth0, wlan0, or lo0.
        Later Linuxes return a descriptive id that contains a physical slot.

            Windows 7
                Ix    Value
                --    -----
                0    "{EF4795CF-8D57-463B-B8C2-10CD2804396D}";
                1    "{59F2EEE3-780E-4B30-80B2-EB8216CC63B6}";
                2    "{5A910E84-B99A-43FF-A257-67149139B4AF}";
                3    "{EA594141-246C-4537-B0CF-DA1DDCDD956C}";

        @return: a list of interface names
        """
        l_interface_names = netifaces.interfaces()
        return l_interface_names

    @staticmethod
    def _find_addr_family_name(p_ix):
        """Returns the string of the family nemr for a given index.
        -1000 = AF_LINK - The MAC address
        2 = AF_INET - IPv4
        23 = AF_INET6 - IPv6
        """
        l_name = netifaces.address_families[p_ix]
        return l_name

    @staticmethod
    def _find_addr_lists(p_interface_name):
        """
        @return:  a dict with the key = interface type (-1000 = MAC Addr, 2 = INET, 23 = INET6)
                    The values are a list of dicts of addresses for that interface.
        """
        l_ret = netifaces.ifaddresses(p_interface_name)
        return l_ret

    @staticmethod
    def _get_address_list(p_list):
        # print(PrettyFormatAny.form(p_list, 'Address'))
        l_list = []
        for l_ent in p_list:
            l_list.append(l_ent['addr'])
        return l_list

    @staticmethod
    def _get_one_interface(p_interface_name):
        """ Gather the information about a single interface given the interfave name.
        """
        l_interface = NodeInterfaceData()
        l_interface.Name = p_interface_name
        l_interface.Active = True
        l_interface.UUID = '123'
        l_interface.NodeInterfaceType = 'Other'
        l_ifs = Interfaces._find_addr_lists(p_interface_name)
        # print(PrettyFormatAny.form(l_ifs, 'Ifs'))
        for l_af in Interfaces._find_addr_lists(p_interface_name).iterkeys():
            if Interfaces._find_addr_family_name(l_af) == 'AF_PACKET':
                l_interface.MacAddress = Interfaces._find_addr_lists(p_interface_name)[l_af]
            if Interfaces._find_addr_family_name(l_af) == 'AF_INET':
                l_interface.V4Address = Interfaces._get_address_list(Interfaces._find_addr_lists(p_interface_name)[l_af])
            if Interfaces._find_addr_family_name(l_af) == 'AF_INET6':
                l_interface.V6Address = Interfaces._get_address_list(Interfaces._find_addr_lists(p_interface_name)[l_af])
        if l_interface.V4Address == [] and l_interface.V6Address == []:
            return
        return l_interface

    @staticmethod
    def _get_all_interfaces():
        """
        @return: a dict of interfaces for this node.
        """
        l_count = 0
        l_dict = {}
        for l_interface_name in Interfaces.find_all_interface_names():
            l_iface = Interfaces._get_one_interface(l_interface_name)
            l_iface.Key = l_count
            l_dict[l_count] = l_iface
            l_count += 1
        LOG.info('Added {} Interfaces to local node'.format(l_count))
        return l_dict


class HandleNodeType(object):

    m_node = NODE_NOTHING

    def __init__(self, p_role):
        self.find_node_type(p_role)

    def init_node_type(self, p_pyhouse_obj):
        if self.m_node & NODE_PIFACECAD:
            self._init_ir_control(p_pyhouse_obj)


    def _init_ir_control(self, p_pyhouse_obj):
        """This node has an IR receiver so set it up.
        """
        l_ir = ir_control.API()
        l_ir.Start(p_pyhouse_obj)



class Util(object):

    @staticmethod
    def _is_camera_node():
        """
        Test to see if this node has a camera attached
        """
        l_ret = NODE_NOTHING
        return l_ret

    @staticmethod
    def _is_controller_node():
        """
        Test to see if this node has a controller attached
        """
        l_ret = NODE_NOTHING
        for l_file in os.listdir('/dev'):
            # Test for lights
            if fnmatch.fnmatch(l_file, 'ttyUSB?'):
                l_ret |= NODE_LIGHTS
                LOG.info('Lighting Node')
        return l_ret

    @staticmethod
    def _is_ir_node():
        """
        Test to see if this node has an IR sensor attached.
        I only have a PiFace-CAD attached
        """
        l_ret = NODE_NOTHING
        for l_file in os.listdir('/dev'):
            if fnmatch.fnmatch(l_file, 'lirc?'):
                l_ret |= NODE_PIFACECAD
                LOG.info('Lirc Node')
        return l_ret

    @staticmethod
    def _is_pandora_node():
        """
        Test to see if this node is a Pandora player
        """
        l_ret = NODE_NOTHING
        if os.path.exists('/usr/bin/pianobar'):
            l_ret |= NODE_PANDORA
            LOG.info('This node is a Pandora Player Node')
        return l_ret

    @staticmethod
    def _is_v6_router_node():
        l_ret = NODE_NOTHING
        return l_ret

    @staticmethod
    def _is_tunnel_node():
        l_ret = NODE_NOTHING
        return l_ret

    @staticmethod
    def _unix_node_test(p_role):
        p_role |= Util._is_camera_node()
        p_role |= Util._is_controller_node()
        p_role |= Util._is_ir_node()
        p_role |= Util._is_pandora_node()
        p_role |= Util._is_v6_router_node()
        p_role |= Util._is_tunnel_node()
        return p_role

    @staticmethod
    def _get_node_info():
        l_node = NodeData()
        l_node.Name = platform.node()
        l_node.Key = 0
        l_node.Active = True
        return l_node

    @staticmethod
    def find_node_role():
        l_role = NODE_NOTHING
        try:
            Util._unix_node_test(l_role)
        except WindowsError:
            l_role |= NODE_WINDOWS
            LOG.info('Windows Node')
        return l_role

    def init_node_type(self, p_pyhouse_obj):
        l_role = p_pyhouse_obj.Computer.Nodes[0].NodeRole
        if l_role & NODE_PIFACECAD:
            self._init_ir_control(p_pyhouse_obj)
        elif l_role & NODE_LIGHTS:
            pass
        elif l_role & NODE_CAMERA:
            pass

    def _init_ir_control(self, p_pyhouse_obj):
        """This node has an IR receiver so set it up.
        """
        l_ir = ir_control.API()
        l_ir.Start(p_pyhouse_obj)

    def insert_node(self, p_node, p_pyhouse_obj):
        return
        """The local node should always be node 0 - Do I want to force it ???
        """
        l_max_key = -1
        try:
            for l_node in p_pyhouse_obj.Computer.Nodes.itervalues():
                if l_node.Name == p_node.Name:
                    p_pyhouse_obj.Computer.Nodes[l_node.Key] = p_node
                    return
                if l_node.Key > l_max_key:
                    l_max_key = l_node.Key
        except AttributeError:
            pass
        p_pyhouse_obj.Computer.Nodes[l_max_key + 1] = p_node
        LOG.info('Nodes = {}'.format(p_pyhouse_obj.Compute.Nodes))

    @staticmethod
    def create_local_node(p_pyhouse_obj):
        l_node = Util._get_node_info()
        l_node.NodeInterfaces = Interfaces._get_all_interfaces()
        l_node.NodeRole = Util.find_node_role()
        return l_node


class API(Util):

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def Start(self):
        # self.m_pyhouse_obj.Computer.Nodes = self.LoadXml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Nodes[0] = Util.create_local_node(self.m_pyhouse_obj)
        self.init_node_type(self.m_pyhouse_obj)

    def Stop(self):
        LOG.info("Stopped.")

    def LoadXml(self, p_pyhouse_obj):
        """ Load the Mqtt xml info.
        """
        pass

    def SaveXml(self, p_xml):
        pass

# ## END DBK
