"""
@name:      PyHouse/src/Modules/Computer/Nodes/test/test_nodes_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 15, 2014
@Summary:

Passed all 9 tests - DBK - 2015-08-14

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData, NodeInterfaceData
from Modules.Computer.Nodes.nodes_xml import Xml as nodesXml
from Modules.Computer.Nodes.test.xml_nodes import \
        TESTING_NODES_NODE_NAME_0, \
        TESTING_NODES_INTERFACE_NAME_0_0, \
        TESTING_NODES_INTERFACE_KEY_0_0, \
        TESTING_NODES_INTERFACE_ACTIVE_0_0, TESTING_NODES_INTERFACE_MAC_ADDRESS_0_0, TESTING_NODES_INTERFACE_ADDRESS_V4_0_0, \
    TESTING_NODES_INTERFACE_ADDRESS_V6_0_0, TESTING_NODES_INTERFACE_NAME_0_1
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = nodesXml()


class FakeNetiface(object):
    """
    """


class A1_Structure(SetupMixin, unittest.TestCase):
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


class B1_Read(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_OneInterface(self):
        l_interface = nodesXml._read_one_interface_xml(self.m_xml.interface)
        print(PrettyFormatAny.form(l_interface, 'Interface'))
        self.assertEqual(l_interface.Name, TESTING_NODES_INTERFACE_NAME_0_0, 'Bad Name')
        self.assertEqual(l_interface.Key, int(TESTING_NODES_INTERFACE_KEY_0_0), 'Bad Key')
        self.assertEqual(l_interface.Active, bool(TESTING_NODES_INTERFACE_ACTIVE_0_0), 'Bad Active')
        self.assertEqual(l_interface.MacAddress, TESTING_NODES_INTERFACE_MAC_ADDRESS_0_0, 'Bad MacAddress')
        self.assertEqual(l_interface.V4Address, TESTING_NODES_INTERFACE_ADDRESS_V4_0_0, 'Bad V4Address')
        self.assertEqual(l_interface.V6Address, TESTING_NODES_INTERFACE_ADDRESS_V6_0_0)

    def test_02_AllInterfaces(self):
        l_interfaces = nodesXml._read_interfaces_xml(self.m_xml.interface_sect)
        print(PrettyFormatAny.form(l_interfaces, 'Interfaces'))
        self.assertEqual(len(l_interfaces), 3)
        self.assertEqual(l_interfaces[0].Name, TESTING_NODES_INTERFACE_NAME_0_0, 'Bad Name')
        self.assertEqual(l_interfaces[1].Name, TESTING_NODES_INTERFACE_NAME_0_1, 'Bad Name')
        self.assertEqual(l_interfaces[2].Name, 'lo', 'Bad Name')
        self.assertEqual(len(l_interfaces), 3, 'Wrong interface count.')

    def test_03_OneNode(self):
        l_node = nodesXml._read_one_node_xml(self.m_xml.node)
        print(PrettyFormatAny.form(l_node, 'One Node'))
        self.assertEqual(l_node.Name, TESTING_NODES_NODE_NAME_0, 'Bad Name')
        self.assertEqual(l_node.Key, 0, 'Bad Key')
        self.assertEqual(l_node.Active, True, 'Bad Active')
        self.assertEqual(l_node.NodeRole, 0, 'Bad NodeRole')

    def test_04_AllNodes(self):
        l_nodes = nodesXml.read_all_nodes_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_nodes, 'All Nodes', 10))
        print(PrettyFormatAny.form(l_nodes[0], 'Node 0', 10))
        print(PrettyFormatAny.form(l_nodes[0].NodeInterfaces, 'All Nodes', 10))
        self.assertEqual(len(l_nodes), 2)



class C03_Write(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_OneInterface(self):
        l_interface = nodesXml._read_one_interface_xml(self.m_xml.interface)
        l_xml = nodesXml._write_one_interface_xml(l_interface)
        print(PrettyFormatAny.form(l_xml, 'One Interface'))
        self.assertEqual(l_xml.attrib['Name'], 'eth0')
        self.assertEqual(l_xml.attrib['Key'], '0')
        self.assertEqual(l_xml.attrib['Active'], 'True')

    def test_02_AllInterfaces(self):
        l_interfaces = nodesXml._read_interfaces_xml(self.m_xml.interface_sect)
        l_xml = nodesXml._write_interfaces_xml(l_interfaces)
        print(PrettyFormatAny.form(l_xml, 'All Interfaces'))

    def test_03_OneNode(self):
        l_node = nodesXml._read_one_node_xml(self.m_xml.node)
        l_xml = nodesXml._write_one_node_xml(l_node)
        print(PrettyFormatAny.form(l_xml, 'All Interfaces'))
        self.assertEqual(l_xml.attrib['Name'], 'pi-01')
        self.assertEqual(l_xml.attrib['Key'], '0')
        self.assertEqual(l_xml.attrib['Active'], 'True')

    def test_04_AllNodes(self):
        l_nodes = nodesXml.read_all_nodes_xml(self.m_pyhouse_obj)
        l_xml = nodesXml.write_nodes_xml(l_nodes)
        print(PrettyFormatAny.form(l_xml, 'All Interfaces'))

# ## END DBK
