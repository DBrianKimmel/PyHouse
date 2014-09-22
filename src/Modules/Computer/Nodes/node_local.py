"""
-*- test-case-name: PyHouse.src.Modules.Core.test.test_node_local -*-

@name: PyHouse/src/Modules/Core/node_local.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@note: Created on Apr 2, 2014
@license: MIT License
@summary: Gather this node's information.

This module:
    Gathers information about the interfaces (ethernet, wifi etc.) on this node.
    Gathers information about the controller devices attached to this node.
    Gathers information about the specialized PyHouse software installed on this node.
    Saves all the gathered information in PyHouseData.
    Starts services on the local node (i.e. ir_service).

The discovered services may be fooled by non PyHouse devices plugged into the computer
  so it is possible to override the role via configuration.
Once overridden the new role will "stick" by being written into the local XML file.
"""

# Import system type stuff
import fnmatch
import netifaces
import os
import platform
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData, NodeInterfaceData
from Modules.Communication import ir_control
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities.xml_tools import XmlConfigTools


g_debug = 0
LOG = Logger.getLogger('PyHouse.NodeLocal   ')


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


class GetAllInterfaceData(object):
    """
    Loop thru all the interfaces and extract the info.

    Netifaces does not define the names we use ( interfaces(), address_families[], ifaddresses() ) so
     we end up with import type errors in this class.
    """

    def __init__(self):
        """
        @type p_node: C{NodeData}
        @param p_node: the node information
        """
        self.m_count = 0
        for l_interface_name in self._find_all_interface_names():
            self._get_one_interface(l_interface_name, self.m_count)
            self.m_count += 1

    def _find_all_interface_names(self):
        """
        This returns a list of interface names.
        """
        l_interface_names = netifaces.interfaces()
        return l_interface_names

    def _find_addr_family_name(self, p_ix):
        l_name = netifaces.address_families[p_ix]
        return l_name

    def _find_addr_lists(self, p_interface_name):
        l_ret = netifaces.ifaddresses(p_interface_name)
        return l_ret

    def _get_address_list(self, p_list):
        l_list = []
        for l_ent in p_list:
            l_list.append(l_ent['addr'])
        return l_list

    def _get_one_interface(self, p_interface_name, p_ix):
        l_interface = NodeInterfaceData()
        l_interface.Name = p_interface_name
        l_interface.Key = p_ix
        l_interface.Active = True
        l_interface.UUID = '123'
        l_interface.NodeInterfaceType = 'Other'
        for l_af in self._find_addr_lists(p_interface_name):
            # print('l_af =', l_af)
            if self._find_addr_family_name(l_af) == 'AF_PACKET':
                l_interface.MacAddress = self._get_address_list(self._find_addr_lists(p_interface_name)[l_af])
            if self._find_addr_family_name(l_af) == 'AF_INET':
                l_interface.V4Address = self._get_address_list(self._find_addr_lists(p_interface_name)[l_af])
            if self._find_addr_family_name(l_af) == 'AF_INET6':
                l_interface.V6Address = self._get_address_list(self._find_addr_lists(p_interface_name)[l_af])
        if l_interface.V4Address == [] and l_interface.V6Address == []:
            return
        # LOG.info("\n\t\t\tInterface:{0:}\n\t\t\tMac:{1:}\n\t\t\tV4:{2:}\n\t\t\tV6:{3:}".format(l_interface.Name, l_interface.MacAddress, l_interface.V4Address, l_interface.V6Address))
        return l_interface

    def get_all_interfaces(self, p_node):
        self.m_count = 0
        for l_interface_name in self._find_all_interface_names():
            l_iface = self._get_one_interface(l_interface_name, self.m_count)
            p_node.NodeInterfaces[self.m_count] = l_iface
            self.m_count += 1
        return p_node


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


class ReadWriteConfigXml(XmlConfigTools):

    m_count = 0
    m_count1 = 0

    def _read_one_interface_xml(self, p_interface_element):
        l_interface_obj = NodeInterfaceData()
        self.read_base_object_xml(l_interface_obj, p_interface_element)
        l_interface_obj.MacAddress = self.get_text_from_xml(p_interface_element, 'MacAddress')
        l_interface_obj.V4Address = self.get_text_from_xml(p_interface_element, 'IPv4Address')
        l_interface_obj.V6Address = self.get_text_from_xml(p_interface_element, 'IPv6Address')
        return l_interface_obj

    def _read_interfaces_xml(self, p_interfaces_xml):
        self.m_count = 0
        l_ret = {}
        try:
            for l_node_xml in p_interfaces_xml.iterfind('Interface'):
                l_node = self._read_one_interface_xml(l_node_xml)
                l_ret[self.m_count] = l_node
                self.m_count += 1
        except AttributeError:
            l_ret = {}
        return l_ret

    def _read_one_node_xml(self, p_node_xml):
        """
        Read the existing XML file (if it exists) and get the node info.
        """
        l_node_obj = NodeData()
        self.read_base_object_xml(l_node_obj, p_node_xml)
        l_node_obj.ConnectionAddr_IPv4 = self.get_text_from_xml(p_node_xml, 'ConnectionAddressV4')
        l_node_obj.ConnectionAddr_IPv6 = self.get_text_from_xml(p_node_xml, 'ConnectionAddressV6')
        l_node_obj.NodeRole = self.get_int_from_xml(p_node_xml, 'NodeRole')
        try:
            l_node_obj.NodeInterfaces = self._read_interfaces_xml(p_node_xml.find('InterfaceSection'))
        except:
            pass
        return l_node_obj

    def read_all_nodes_xml(self, p_pyhouse_obj):
        l_comp = p_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision')
        self.m_count_nodes = 0
        l_ret = {}
        try:
            l_xml = l_comp.find('NodeSection')
            for l_node_xml in l_xml.iterfind('Node'):
                l_node = self._read_one_node_xml(l_node_xml)
                l_ret[self.m_count_nodes] = l_node
                self.m_count_nodes += 1
        except AttributeError as e_err:
            print('ERROR - Node read error - {0:}'.format(e_err))
        return l_ret


    def _write_one_interface_xml(self, p_interface_obj):
        l_entry = self.write_base_object_xml('Interface', p_interface_obj)
        self.put_text_element(l_entry, 'MacAddress', p_interface_obj.MacAddress)
        self.put_text_element(l_entry, 'IPv4Address', p_interface_obj.V4Address)
        self.put_text_element(l_entry, 'IPv6Address', p_interface_obj.V6Address)
        return l_entry

    def _write_interfaces_xml(self, p_interfaces_obj):
        l_xml = ET.Element('InterfaceSection')
        self.m_count = 0
        for l_interface_obj in p_interfaces_obj.itervalues():
            l_entry = self._write_one_interface_xml(l_interface_obj)
            l_xml.append(l_entry)
            self.m_count += 1
        return l_xml

    def _write_one_node_xml(self, p_node_obj):
        l_entry = self.write_base_object_xml('Node', p_node_obj)
        self.put_text_element(l_entry, 'ConnectionAddressV4', p_node_obj.ConnectionAddr_IPv4)
        self.put_int_element(l_entry, 'NodeRole', p_node_obj.NodeRole)
        l_entry.append(self._write_interfaces_xml(p_node_obj.NodeInterfaces))
        return l_entry

    def write_nodes_xml(self, p_nodes_obj):
        l_xml = ET.Element('NodeSection')
        self.m_count1 = 0
        for l_node_obj in p_nodes_obj.itervalues():
            l_entry = self._write_one_node_xml(l_node_obj)
            l_xml.append(l_entry)
            self.m_count1 += 1
        return l_xml


class Utility(ReadWriteConfigXml):

    def _is_camera_node(self):
        """
        Test to see if this node has a camera attached
        """
        l_ret = NODE_NOTHING
        return l_ret

    def _is_controller_node(self):
        """
        Test to see if this node has a controller attached
        """
        l_ret = NODE_NOTHING
        for l_file in os.listdir('/dev'):
            # Test for lights
            if fnmatch.fnmatch(l_file, 'ttyUSB?'):
                l_ret |= NODE_LIGHTS
                LOG.debug('Lighting Node')
        return l_ret

    def _is_ir_node(self):
        """
        Test to see if this node has an IR sensor attached.
        I only have a PiFace-CAD attached
        """
        l_ret = NODE_NOTHING
        for l_file in os.listdir('/dev'):
            if fnmatch.fnmatch(l_file, 'lirc?'):
                l_ret |= NODE_PIFACECAD
                LOG.debug('Lirc Node')
        return l_ret

    def _is_pandora_node(self):
        """
        Test to see if this node is a Pandora player
        """
        l_ret = NODE_NOTHING
        if os.path.exists('/usr/bin/pianobar'):
            l_ret |= NODE_PANDORA
            LOG.debug('This node is a Pandora Player Node')
        return l_ret

    def _is_v6_router_node(self):
        l_ret = NODE_NOTHING
        return l_ret

    def _is_tunnel_node(self):
        l_ret = NODE_NOTHING
        return l_ret

    def _unix_node_test(self, p_role):
        p_role |= self._is_camera_node()
        p_role |= self._is_controller_node()
        p_role |= self._is_ir_node()
        p_role |= self._is_pandora_node()
        p_role |= self._is_v6_router_node()
        p_role |= self._is_tunnel_node()
        return p_role

    def get_node_info(self, p_pyhouse_obj):
        p_pyhouse_obj.Computer.Nodes[0].Name = platform.node()
        p_pyhouse_obj.Computer.Nodes[0].Key = 0
        p_pyhouse_obj.Computer.Nodes[0].Active = True

    def find_node_role(self):
        l_role = NODE_NOTHING
        try:
            self._unix_node_test(l_role)
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
        if g_debug >= 1:
            LOG.debug('Nodes = {0:}'.format(p_pyhouse_obj.Compute.Nodes))

    def create_local_node(self):
        l_node = NodeData()
        l_api = GetAllInterfaceData()
        l_api.get_all_interfaces(l_node)
        return l_node


class API(Utility):

    m_pyhouse_obj = None

    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.read_all_nodes_xml(p_pyhouse_obj)
        p_pyhouse_obj.Computer.Nodes[0] = self.create_local_node()
        self.get_node_info(p_pyhouse_obj)
        p_pyhouse_obj.Computer.Nodes[0].NodeRole = self.find_node_role()
        self.init_node_type(p_pyhouse_obj)

    def Stop(self):
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        p_xml.append(self.write_nodes_xml(self.m_pyhouse_obj.Computer.Nodes))
        LOG.info("Saved XML.")

# ## END DBK
