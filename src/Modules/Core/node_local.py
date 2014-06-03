"""
-*- test-case-name: PyHouse.src.Modules.Core.test.test_node_local -*-

@name: PyHouse/src/Modules/Core/node_local.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@note: Created on Apr 2, 2014
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
import netifaces
import os
import platform
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData, NodeInterfaceData
from Modules.communication import ir_control
from Modules.utils.xml_tools import PutGetXML, ConfigTools
from Modules.utils import pyh_log

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.NodeLocal   ')


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
            l_interface = NodeInterfaceData()
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
            LOG.info("Interface:{0:}, Mac:{1:}, V4:{2:}, V6:{3:} - {4:}".format(l_interface.Name, l_interface.MacAddress, l_interface.V4Address, l_interface.V6Address, l_count))
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


class XML(ConfigTools):

    m_count = 0

    def read_one_interface_xml(self, p_interface_element):
        l_interface_obj = NodeInterfaceData()
        self.read_base_object_xml(l_interface_obj, p_interface_element)
        l_interface_obj.MacAddress = self.get_text_from_xml(p_interface_element, 'MacAddress')
        l_interface_obj.V4Address = self.get_text_from_xml(p_interface_element, 'IPv4Address')
        l_interface_obj.V6Address = self.get_text_from_xml(p_interface_element, 'IPv6Address')
        return l_interface_obj

    def read_interfaces_xml(self, p_interfaces_xml):
        self.m_count = 0
        l_ret = {}
        try:
            for l_node_xml in p_interfaces_xml.iterfind('Interface'):
                l_node = self.read_one_interface_xml(l_node_xml)
                l_ret[self.m_count] = l_node
                self.m_count += 1
        except AttributeError:
            l_ret = {}
        return l_ret

    def write_one_interface_xml(self, p_interface_obj):
        l_entry = self.write_base_object_xml('Interface', p_interface_obj)
        self.put_text_element(l_entry, 'MacAddress', p_interface_obj.MacAddress)
        self.put_text_element(l_entry, 'IPv4Address', p_interface_obj.V4Address)
        self.put_text_element(l_entry, 'IPv6Address', p_interface_obj.V6Address)
        return l_entry

    def write_interfaces_xml(self, p_interfaces_obj):
        l_xml = ET.Element('Interfaces')
        self.m_count = 0
        for l_interface_obj in p_interfaces_obj.itervalues():
            l_entry = self.write_one_interface_xml(l_interface_obj)
            l_xml.append(l_entry)
            self.m_count += 1
        return l_xml

    def read_one_node_xml(self, p_node_xml):
        """
        Read the existing XML file (if it exists) and get the node info.
        """
        l_node_obj = NodeData()
        self.read_base_object_xml(l_node_obj, p_node_xml)
        l_node_obj.ConnectionAddr_IPv4 = self.get_text_from_xml(p_node_xml, 'ConnectionAddressV4')
        l_node_obj.Role = self.get_int_from_xml(p_node_xml, 'Role')
        l_node_obj.Interfaces = self.read_interfaces_xml(p_node_xml.find('Interfaces'))
        return l_node_obj

    def read_nodes_xml(self, p_nodes_xml):
        self.m_count = 0
        l_ret = {}
        try:
            for l_node_xml in p_nodes_xml.iterfind('Node'):
                l_node = self.read_one_node_xml(l_node_xml)
                l_ret[self.m_count] = l_node
                self.m_count += 1
        except:
            pass
        return l_ret

    def write_one_node_xml(self, p_node_obj):
        l_entry = self.write_base_object_xml('Node', p_node_obj)
        self.put_text_element(l_entry, 'ConnectionAddressV4', p_node_obj.ConnectionAddr_IPv4)
        self.put_int_element(l_entry, 'Role', p_node_obj.Role)
        l_entry.append(self.write_interfaces_xml(p_node_obj.Interfaces))
        return l_entry

    def write_nodes_xml(self, p_nodes_obj):
        l_xml = ET.Element('Nodes')
        self.m_count = 0
        for l_node_obj in p_nodes_obj.itervalues():
            l_entry = self.write_one_node_xml(l_node_obj)
            l_xml.append(l_entry)
            self.m_count += 1
        return l_xml



class Utility(XML):

    def get_node_info(self, p_pyhouses_obj):
        p_pyhouses_obj.Nodes[0].Name = platform.node()
        p_pyhouses_obj.Nodes[0].Key = 0
        p_pyhouses_obj.Nodes[0].Active = True

    def find_node_role(self):
        p_role = NODE_NOTHING
        try:
            for l_file in os.listdir('/dev'):
                # Test for lights
                if fnmatch.fnmatch(l_file, 'ttyUSB?'):
                    p_role |= NODE_LIGHTS
                    LOG.debug('Lighting Node')
                if fnmatch.fnmatch(l_file, 'lirc?'):
                    p_role |= NODE_PIFACECAD
                    LOG.debug('Lirc Node')
            # Test for Pandora
            if os.path.exists('/usr/bin/pianobar'):
                p_role |= NODE_PANDORA
                LOG.debug('Pandora Node')
            # Test for camera
            #
        except WindowsError:
            p_role |= NODE_WINDOWS
            LOG.debug('Windows Node')
        return p_role

    def init_node_type(self, p_pyhouses_obj):
        l_role = p_pyhouses_obj.Nodes[0].Role
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
            for l_node in p_pyhouses_obj.Nodes.itervalues():
                if l_node.Name == p_node.Name:
                    p_pyhouses_obj.Nodes[l_node.Key] = p_node
                    return
                if l_node.Key > l_max_key:
                    l_max_key = l_node.Key
        except AttributeError:
            pass
        p_pyhouses_obj.Nodes[l_max_key + 1] = p_node
        LOG.debug('Nodes = {0:}'.format(p_pyhouses_obj.Nodes))


class API(Utility):

    m_node = None
    m_pyhouses_obj = None

    def __init__(self):
        pass

    def Start(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj
        self.m_node = NodeData()
        GetAllInterfaceData(self.m_node)
        p_pyhouses_obj.Nodes[0] = self.m_node
        self.read_nodes_xml(p_pyhouses_obj.XmlRoot.find('Nodes'))
        self.get_node_info(p_pyhouses_obj)
        p_pyhouses_obj.Nodes[0].Role = self.find_node_role()
        self.init_node_type(p_pyhouses_obj)
        LOG.info('Started')

    def Stop(self, p_xml):
        p_xml.append(self.write_nodes_xml(self.m_pyhouses_obj.Nodes))
        LOG.info("XML appended.")

# ## END DBK
