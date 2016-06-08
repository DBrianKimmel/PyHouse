"""
@name:      PyHouse/src/Modules/Computer/Nodes/nodes_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 15, 2014
@Summary:

PyHouse_obj.Computer.Nodes is a dict of nodes.


"""

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Core.data_objects import NodeData, NodeInterfaceData
from Modules.Utilities.xml_tools import PutGetXML, XmlConfigTools
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities.debug_tools import PrettyFormatAny
# from Modules.Utilities.debug_tools import PrettyFormatAny

LOG = Logger.getLogger('PyHouse.Nodes_xml      ')


class Xml(object):

    @staticmethod
    def _read_one_interface_xml(p_interface_element):
        l_interface_obj = NodeInterfaceData()
        XmlConfigTools.read_base_object_xml(l_interface_obj, p_interface_element)
        l_interface_obj.MacAddress = PutGetXML.get_text_from_xml(p_interface_element, 'MacAddress')
        l_interface_obj.V4Address = PutGetXML.get_text_from_xml(p_interface_element, 'IPv4Address')
        l_interface_obj.V6Address = PutGetXML.get_text_from_xml(p_interface_element, 'IPv6Address')
        l_interface_obj.NodeInterfaceType = PutGetXML.get_text_from_xml(p_interface_element, 'InterfaceType')
        return l_interface_obj

    @staticmethod
    def _write_one_interface_xml(p_interface_obj):
        l_entry = XmlConfigTools.write_base_object_xml('Interface', p_interface_obj)
        PutGetXML.put_text_element(l_entry, 'MacAddress', p_interface_obj.MacAddress)
        PutGetXML.put_text_element(l_entry, 'IPv4Address', p_interface_obj.V4Address)
        PutGetXML.put_text_element(l_entry, 'IPv6Address', p_interface_obj.V6Address)
        return l_entry

    @staticmethod
    def _read_interfaces_xml(p_interfaces_xml):
        l_count = 0
        l_ret = {}
        try:
            for l_node_xml in p_interfaces_xml.iterfind('Interface'):
                l_node = Xml._read_one_interface_xml(l_node_xml)
                l_ret[l_count] = l_node
                l_count += 1
        except AttributeError:
            l_ret = {}
        #  LOG.info("XML Loaded")
        return l_ret

    @staticmethod
    def _write_interfaces_xml(p_interfaces_obj):
        l_xml = ET.Element('InterfaceSection')
        l_count = 0
        for l_interface_obj in p_interfaces_obj.itervalues():
            l_entry = Xml._write_one_interface_xml(l_interface_obj)
            l_xml.append(l_entry)
            l_count += 1
        return l_xml

    @staticmethod
    def _read_one_node_xml(p_node_xml):
        """
        Read the existing XML file (if it exists) and get the node info.
        """
        l_node_obj = NodeData()
        XmlConfigTools.read_base_object_xml(l_node_obj, p_node_xml)
        l_node_obj.ConnectionAddr_IPv4 = PutGetXML.get_text_from_xml(p_node_xml, 'ConnectionAddressV4')
        l_node_obj.ConnectionAddr_IPv6 = PutGetXML.get_text_from_xml(p_node_xml, 'ConnectionAddressV6')
        l_node_obj.NodeRole = PutGetXML.get_int_from_xml(p_node_xml, 'NodeRole')
        l_node_obj.LastUpdate = PutGetXML.get_date_time_from_xml(p_node_xml, 'LastUpdate')
        # print(PrettyFormatAny.form(l_node_obj, 'Node xxx'))
        # print(PrettyFormatAny.form(p_node_xml, 'Node yyy'))
        try:
            l_node_obj.NodeInterfaces = Xml._read_interfaces_xml(p_node_xml.find('InterfaceSection'))
        except AttributeError as e_err:
            LOG.error('ERROR OneNodeRead error {}'.format(e_err))
        return l_node_obj

    @staticmethod
    def _write_one_node_xml(p_node_obj):
        l_entry = XmlConfigTools.write_base_object_xml('Node', p_node_obj)
        PutGetXML.put_text_element(l_entry, 'ConnectionAddressV4', p_node_obj.ConnectionAddr_IPv4)
        PutGetXML.put_text_element(l_entry, 'ConnectionAddressV6', p_node_obj.ConnectionAddr_IPv6)
        PutGetXML.put_int_element(l_entry, 'NodeRole', p_node_obj.NodeRole)
        PutGetXML.put_date_time_element(l_entry, 'LastUpdate', p_node_obj.LastUpdate)
        l_entry.append(Xml._write_interfaces_xml(p_node_obj.NodeInterfaces))
        return l_entry

    @staticmethod
    def read_all_nodes_xml(p_pyhouse_obj):
        l_count = 0
        l_ret = {}
        l_comp = p_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision')
        if l_comp is None:
            LOG.warn('No ComputerDivision')
            return l_ret
        try:
            l_xml = l_comp.find('NodeSection')
            for l_node_xml in l_xml.iterfind('Node'):
                l_node = Xml._read_one_node_xml(l_node_xml)
                l_ret[l_node.Name] = l_node
                l_count += 1
                LOG.info('Loaded Node {}'.format(l_node.Name))
        except AttributeError as e_err:
            l_ret[0] = NodeData()  # Create an empty Nodes[<name>]
            LOG.error('ERROR - Node read error - {}'.format(e_err))
        LOG.info('Loaded {} Nodes'.format(l_count))
        return l_ret

    @staticmethod
    def write_nodes_xml(p_pyhouse_obj):
        l_xml = ET.Element('NodeSection')
        l_nodes = p_pyhouse_obj.Computer.Nodes
        l_msg = PrettyFormatAny.form(l_nodes, 'Nodes')
        LOG.warn('About to write {} nodes  {}'.format(len(l_nodes), l_msg))
        l_count = 0
        for l_node_obj in l_nodes.itervalues():
            try:
                l_entry = Xml._write_one_node_xml(l_node_obj)
                l_xml.append(l_entry)
                l_count += 1
            except AttributeError as e_err:
                LOG.error('Error {}'.format(e_err))
        return l_xml, l_count

#  ## END DBK
