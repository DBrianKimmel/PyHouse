"""
@name:      PyHouse/Project/src/Modules/Computer/Nodes/nodes_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 15, 2014
@Summary:

PyHouse_obj.Computer.Nodes is a dict of nodes.

"""
__updated__ = '2019-06-19'

#  Import system type stuff
import xml.etree.ElementTree as ET
# import datetime

#  Import PyMh files and modules.
from Modules.Core.data_objects import NodeData, NodeInterfaceData, UuidData
from Modules.Core.Utilities.xml_tools import PutGetXML, XmlConfigTools
from Modules.Core.Utilities import uuid_tools
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Nodes_xml      ')

NODE_SECTION = 'NodeSection'
NODE_ATTR = 'Node'


class Xml(object):

    @staticmethod
    def _read_one_interface_xml(p_interface_element):
        l_interface_obj = NodeInterfaceData()
        XmlConfigTools.read_base_UUID_object_xml(l_interface_obj, p_interface_element)
        l_interface_obj.MacAddress = PutGetXML.get_text_from_xml(p_interface_element, 'MacAddress')
        l_interface_obj.V4Address = PutGetXML.get_text_from_xml(p_interface_element, 'IPv4Address')
        l_interface_obj.V6Address = PutGetXML.get_text_from_xml(p_interface_element, 'IPv6Address')
        l_interface_obj.NodeInterfaceType = PutGetXML.get_text_from_xml(p_interface_element, 'InterfaceType')
        return l_interface_obj

    @staticmethod
    def _write_one_interface_xml(p_interface_obj):
        l_entry = XmlConfigTools.write_base_UUID_object_xml('Interface', p_interface_obj)
        PutGetXML.put_text_element(l_entry, 'MacAddress', p_interface_obj.MacAddress)
        PutGetXML.put_text_element(l_entry, 'IPv4Address', p_interface_obj.V4Address)
        PutGetXML.put_text_element(l_entry, 'IPv6Address', p_interface_obj.V6Address)
        PutGetXML.put_text_element(l_entry, 'InterfaceType', p_interface_obj.NodeInterfaceType)
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
        return l_ret

    @staticmethod
    def _write_interfaces_xml(p_interfaces_obj):
        l_xml = ET.Element('InterfaceSection')
        l_count = 0
        if p_interfaces_obj is None:
            return l_xml
        for l_interface_obj in p_interfaces_obj.values():
            l_entry = Xml._write_one_interface_xml(l_interface_obj)
            l_xml.append(l_entry)
            l_count += 1
        return l_xml

    @staticmethod
    def update_add_node():
        """ Put a node into the dict.
        Be sure nodes with the same UUID does not create a duplicate.
        """
        pass

    @staticmethod
    def _read_one_node_xml(p_node_xml):
        """
        Use the passed in xml to create a node entry.

        @param p_node_xml: is the element in the Xml config file that describes a node.
        @return: a node object filled in.
        """
        l_node_obj = NodeData()
        XmlConfigTools.read_base_UUID_object_xml(l_node_obj, p_node_xml)
        l_node_obj.ConnectionAddr_IPv4 = PutGetXML.get_text_from_xml(p_node_xml, 'ConnectionAddressV4')
        l_node_obj.ConnectionAddr_IPv6 = PutGetXML.get_text_from_xml(p_node_xml, 'ConnectionAddressV6')
        l_node_obj.NodeRole = PutGetXML.get_int_from_xml(p_node_xml, 'NodeRole')
        try:
            l_node_obj.NodeInterfaces = Xml._read_interfaces_xml(p_node_xml.find('InterfaceSection'))
        except AttributeError as e_err:
            LOG.error('ERROR OneNodeRead error {}'.format(e_err))
        return l_node_obj

    @staticmethod
    def _write_one_node_xml(p_node_obj):
        l_entry = XmlConfigTools.write_base_UUID_object_xml(NODE_ATTR, p_node_obj)
        PutGetXML.put_text_element(l_entry, 'ConnectionAddressV4', p_node_obj.ConnectionAddr_IPv4)
        PutGetXML.put_text_element(l_entry, 'ConnectionAddressV6', p_node_obj.ConnectionAddr_IPv6)
        PutGetXML.put_int_element(l_entry, 'NodeRole', p_node_obj.NodeRole)
        l_entry.append(Xml._write_interfaces_xml(p_node_obj.NodeInterfaces))
        return l_entry

    @staticmethod
    def read_all_nodes_xml(p_pyhouse_obj):
        """ The key on disk is an integer 0,1,2...
        The Key in PyHouse_obj is the UUID.
        Be careful of confusing the two.
        """
        l_count = 0
        l_ret = {}
        l_xml = XmlConfigTools.find_xml_section(p_pyhouse_obj, 'ComputerDivision')
        if l_xml is None:
            return l_ret
        l_xml = l_xml.find(NODE_SECTION)
        if l_xml is None:
            return l_ret
        for l_node_xml in l_xml.iterfind(NODE_ATTR):
            l_node_obj = Xml._read_one_node_xml(l_node_xml)
            l_node_obj.Key = l_count
            l_ret[l_node_obj.UUID] = l_node_obj
            l_uuid_obj = UuidData()
            l_uuid_obj.UUID = l_node_obj.UUID
            l_uuid_obj.UuidType = 'Node'
            uuid_tools.Uuid.add_uuid(p_pyhouse_obj, l_uuid_obj)
            l_count += 1
            LOG.info('Loaded Node:{}, Key:{}'.format(l_node_obj.Name, l_node_obj.Key))
        LOG.info('Loaded {} Nodes'.format(l_count))
        p_pyhouse_obj.Computer.Nodes = l_ret
        return l_ret

    @staticmethod
    def write_nodes_xml(p_pyhouse_obj):
        """ These are writing in a random order - makes testing not work.
        """
        l_xml = ET.Element(NODE_SECTION)
        l_nodes = p_pyhouse_obj.Computer.Nodes
        l_count = 0
        for l_node_obj in l_nodes.values():
            LOG.info('Writing entry for node {}'.format(l_node_obj.Name))
            try:
                l_node_obj.Key = l_count
                l_entry = Xml._write_one_node_xml(l_node_obj)
                l_xml.append(l_entry)
                l_count += 1
            except AttributeError as e_err:
                LOG.error('Error {}'.format(e_err))
        return l_xml, l_count

#  ## END DBK
