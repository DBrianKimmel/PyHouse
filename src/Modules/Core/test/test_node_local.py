"""
@name: PyHouse/src/Modules/Core/test/test_node_local.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 29, 2014
@summary: This module is for testing local node data.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, CoreServicesData, NodeData, NodeInterfaceData
from Modules.Core import node_local
from Modules.utils import xml_tools
from Modules.utils.tools import PrettyPrintObject, PrettyPrintXML, PrintObject
from src.test import xml_data


class Test_02_ReadWriteXML(unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.CoreServicesData = CoreServicesData()
        self.m_pyhouse_obj.Nodes[0] = NodeData()
        self.m_pyhouse_obj.XmlRoot = self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_nodes_xml = self.m_root_xml.find('Nodes')
        self.m_node_xml = self.m_nodes_xml.find('Node')
        self.m_interfaces_xml = self.m_node_xml.find('Interfaces')
        self.m_interface_xml = self.m_interfaces_xml.find('Interface')
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeData()
        self.m_api = node_local.API()

    def test_0221_read_one_interface(self):
        l_interface = self.m_api.read_one_interface_xml(self.m_interface_xml)
        self.assertEqual(l_interface.Name, 'eth0', 'Bad Name')
        self.assertEqual(l_interface.Key, 0, 'Bad Key')
        self.assertEqual(l_interface.Active, True, 'Bad Active')
        self.assertEqual(l_interface.MacAddress, '01:02:03:04:05:06', 'Bad MacAddress')
        self.assertEqual(l_interface.V4Address, "192.168.1.11", 'Bad V4Address')
        self.assertEqual(l_interface.V6Address, '2000:1D::1, 2000:1D::101', 'Bad V6Address')
        PrettyPrintObject(l_interface)

    def test_0222_read_interfaces(self):
        l_interfaces = self.m_api.read_interfaces_xml(self.m_interfaces_xml)
        self.assertEqual(l_interfaces[0].Name, 'eth0', 'Bad Name')
        self.assertEqual(l_interfaces[1].Name, 'wlan0', 'Bad Name')
        self.assertEqual(l_interfaces[2].Name, 'lo', 'Bad Name')
        self.assertEqual(len(l_interfaces), 3, 'Wrong interface count.')

    def test_0231_write_one_interface(self):
        l_interface = self.m_api.read_one_interface_xml(self.m_interface_xml)
        l_xml = self.m_api.write_one_interface_xml(l_interface)
        PrettyPrintXML(l_xml)

    def test_0232_write_interfaces(self):
        l_interfaces = self.m_api.read_interfaces_xml(self.m_interfaces_xml)
        l_xml = self.m_api.write_interfaces_xml(l_interfaces)
        PrettyPrintXML(l_xml)

    def test_0241_read_one_node(self):
        l_node = self.m_api.read_one_node_xml(self.m_node_xml)
        self.assertEqual(l_node.Name, 'PiNode-1', 'Bad Name')
        self.assertEqual(l_node.Key, 0, 'Bad Key')
        self.assertEqual(l_node.Active, True, 'Bad Axtive')
        self.assertEqual(l_node.Role, 0, 'Bad Role')
        PrettyPrintObject(l_node)

    def test_0242_read_nodes(self):
        l_nodes = self.m_api.read_nodes_xml(self.m_nodes_xml)
        print('Nodes: {0:}'.format((l_nodes)))
        PrettyPrintObject(l_nodes)
        PrintObject('--title--', l_nodes)

    def test_0251_write_one_node(self):
        l_node = self.m_api.read_one_node_xml(self.m_node_xml)
        l_xml = self.m_api.write_one_node_xml(l_node)
        PrettyPrintXML(l_xml)

    def test_0252_write_nodes(self):
        l_nodes = self.m_api.read_nodes_xml(self.m_nodes_xml)
        l_xml = self.m_api.write_nodes_xml(l_nodes)
        PrettyPrintXML(l_xml)


class Test_03_ReadWriteEmptyXML(unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.CoreServicesData = CoreServicesData()
        self.m_pyhouse_obj.Nodes[0] = NodeData()
        self.m_pyhouse_obj.XmlRoot = self.m_root_xml = ET.fromstring(xml_data.XML_EMPTY)
        self.m_nodes_xml = self.m_root_xml.find('Nodes')
        self.m_node_xml = None
        self.m_interfaces_xml = None
        self.m_interface_xml = None
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeData()
        self.m_api = node_local.API()

    def test_0221_read_one_interface(self):
        l_interface = self.m_api.read_one_interface_xml(self.m_interface_xml)
        self.assertEqual(l_interface.Name, None, 'Bad Name')
        PrettyPrintObject(l_interface)

    def test_0222_read_interfaces(self):
        l_interfaces = self.m_api.read_interfaces_xml(self.m_interfaces_xml)
        self.assertEqual(l_interfaces, {}, 'Bad Name')

    def test_0242_read_nodes(self):
        l_nodes = self.m_api.read_nodes_xml(self.m_nodes_xml)
        print('Nodes: {0:}'.format((l_nodes)))
        PrettyPrintObject(l_nodes)
        PrintObject('--title--', l_nodes)

    def test_0252_write_nodes(self):
        l_nodes = self.m_api.read_nodes_xml(self.m_nodes_xml)
        l_xml = self.m_api.write_nodes_xml(l_nodes)
        PrettyPrintXML(l_xml)


class Test_10_ApiStart(unittest.TestCase):

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.CoreServicesData = CoreServicesData()
        self.m_pyhouse_obj.Nodes[0] = NodeData()
        self.m_pyhouse_obj.XmlRoot = self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_root_element = self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_util = xml_tools.PutGetXML()
        self.m_pyhouse_obj = PyHouseData()
        self.m_api = node_local.API()

    def test_1001_Init(self):
        self.m_api

    def test_1002_Start(self):
        self.m_api.Start(self.m_pyhouse_obj)

    def test_1003_Stop(self):
        self.m_api.Stop(self.m_root_xml)

# ## END DBK
