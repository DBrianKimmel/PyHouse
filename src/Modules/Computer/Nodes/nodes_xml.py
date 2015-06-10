"""
@name: PyHouse/src/Modules/Computer/Nodes/nodes_xml.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Dec 15, 2014
@Summary:

"""


# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData, NodeInterfaceData
from Modules.Utilities.xml_tools import XmlConfigTools
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Nodes_xml      ')


class Xml(XmlConfigTools):

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
        LOG.info("XML Loaded")
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
        except AttributeError as e_err:
            print('ERROR OneNodeRead error {}'.format(e_err))
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
        self.put_text_element(l_entry, 'ConnectionAddressV6', p_node_obj.ConnectionAddr_IPv6)
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

# ## END DBK
