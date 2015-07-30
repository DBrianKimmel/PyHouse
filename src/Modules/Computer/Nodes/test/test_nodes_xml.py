"""
@name:      PyHouse/src/Modules/Computer/Nodes/test/test_nodes_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 15, 2014
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData, NodeInterfaceData
from Modules.Computer.Nodes import nodes_xml
from Modules.Computer.Nodes.test.xml_nodes import TESTING_NODES_NODE_NAME_1
# from test.xml_data import *
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG, XML_EMPTY
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = nodes_xml.Xml()


class FakeNetiface(object):
    """
    """


class C01_Structure(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeData()

    def test_01_PyHouse(self):
        # PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse')
        # PrettyPrintAny(self.m_pyhouse_obj.Computer, 'Computer')
        # PrettyPrintAny(self.m_xml.computer_div, 'ComputerDiv XML')
        # PrettyPrintAny(self.m_xml.node_sect, 'NodeSect XML')
        # PrettyPrintAny(self.m_xml.node, 'Node XML')
        pass


class C02_Read(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_OneInterface(self):
        l_interface = self.m_api._read_one_interface_xml(self.m_xml.interface)
        # PrettyPrintAny(l_interface, 'One Interface')
        self.assertEqual(l_interface.Name, 'eth0', 'Bad Name')
        self.assertEqual(l_interface.Key, 0, 'Bad Key')
        self.assertEqual(l_interface.Active, True, 'Bad Active')
        self.assertEqual(l_interface.MacAddress, '01:02:03:04:05:06', 'Bad MacAddress')
        self.assertEqual(l_interface.V4Address, "192.168.1.11", 'Bad V4Address')
        self.assertEqual(l_interface.V6Address, '2000:1D::1, 2000:1D::101', 'Bad V6Address')

    def test_02_AllInterfaces(self):
        l_interfaces = self.m_api._read_interfaces_xml(self.m_xml.interface_sect)
        # PrettyPrintAny(l_interfaces, 'All Interfaces')
        # PrettyPrintAny(l_interfaces[1], 'Interface_1')
        self.assertEqual(l_interfaces[0].Name, 'eth0', 'Bad Name')
        self.assertEqual(l_interfaces[1].Name, 'wlan0', 'Bad Name')
        self.assertEqual(l_interfaces[2].Name, 'lo', 'Bad Name')
        self.assertEqual(len(l_interfaces), 3, 'Wrong interface count.')

    def test_03_OneNode(self):
        l_node = self.m_api._read_one_node_xml(self.m_xml.node)
        # PrettyPrintAny(l_node, 'One Node', 105)
        self.assertEqual(l_node.Name, TESTING_NODES_NODE_NAME_1, 'Bad Name')
        self.assertEqual(l_node.Key, 0, 'Bad Key')
        self.assertEqual(l_node.Active, True, 'Bad Active')
        self.assertEqual(l_node.NodeRole, 0, 'Bad NodeRole')

    def test_04_AllNodes(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        # PrettyPrintAny(l_nodes, 'All Nodes', 10)
        # PrettyPrintAny(l_nodes[0], 'Node 0', 10)



class C03_Write(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_OneInterface(self):
        l_interface = self.m_api._read_one_interface_xml(self.m_xml.interface)
        l_xml = self.m_api._write_one_interface_xml(l_interface)
        # PrettyPrintAny(l_xml)
        self.assertEqual(l_xml.attrib['Name'], 'eth0')
        self.assertEqual(l_xml.attrib['Key'], '0')
        self.assertEqual(l_xml.attrib['Active'], 'True')

    def test_02_AllInterfaces(self):
        l_interfaces = self.m_api._read_interfaces_xml(self.m_xml.interface_sect)
        l_xml = self.m_api._write_interfaces_xml(l_interfaces)
        # PrettyPrintAny(l_xml)

    def test_03_OneNode(self):
        l_node = self.m_api._read_one_node_xml(self.m_xml.node)
        l_xml = self.m_api._write_one_node_xml(l_node)
        # PrettyPrintAny(l_xml)
        self.assertEqual(l_xml.attrib['Name'], 'pi-01')
        self.assertEqual(l_xml.attrib['Key'], '0')
        self.assertEqual(l_xml.attrib['Active'], 'True')

    def test_04_AllNodes(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_nodes_xml(l_nodes)
        # PrettyPrintAny(l_xml)



class C04_ReadEmpty(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_EMPTY))

    def test_01_OneInterface(self):
        l_interface = self.m_api._read_one_interface_xml(self.m_xml.interface)
        self.assertEqual(l_interface.Name, 'Missing Name', 'Bad Name')
        # PrettyPrintAny(l_interface, 'One empty interface')

    def test_02_AllInterfaces(self):
        l_interfaces = self.m_api._read_interfaces_xml(self.m_xml.interface_sect)
        # PrettyPrintAny(l_interfaces, 'All empty interface')
        self.assertEqual(l_interfaces, {}, 'Bad Name')

    def test_03_OneNode(self):
        l_node = self.m_api._read_one_node_xml(self.m_xml.node)
        # PrettyPrintAny(l_node, 'One empty node')

    def test_04_AllNodes(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        # print('Nodes: {0:}'.format((l_nodes)))
        # PrettyPrintAny(l_nodes, 'All empty nodes')



class C05_WriteEmpty(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_EMPTY))

    def test_01_OneInterface(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_nodes_xml(l_nodes)
        # PrettyPrintAny(l_xml)

    def test_02_AllInterfaces(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_nodes_xml(l_nodes)
        # PrettyPrintAny(l_xml)

    def test_03_OneNode(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_nodes_xml(l_nodes)
        # PrettyPrintAny(l_xml)

    def test_04_All(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_nodes_xml(l_nodes)
        # PrettyPrintAny(l_xml)

# ## END DBK
