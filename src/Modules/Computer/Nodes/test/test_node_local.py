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
from Modules.Core.data_objects import PyHouseData, NodeData, NodeInterfaceData
from Modules.Computer.Nodes import node_local
from Modules.Utilities import xml_tools
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = node_local.API()


class Test_01_Structure(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeData()

    def test_01_PyHouse(self):
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse')
        PrettyPrintAny(self.m_pyhouse_obj.Computer, 'Computer')
        PrettyPrintAny(self.m_pyhouse_obj.Computer.Nodes, 'Nodes')


class Test_02_XML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_ReadOneInterface(self):
        l_interface = self.m_api._read_one_interface_xml(self.m_xml.interface)
        PrettyPrintAny(l_interface, 'One Interface')
        self.assertEqual(l_interface.Name, 'eth0', 'Bad Name')
        self.assertEqual(l_interface.Key, 0, 'Bad Key')
        self.assertEqual(l_interface.Active, True, 'Bad Active')
        self.assertEqual(l_interface.MacAddress, '01:02:03:04:05:06', 'Bad MacAddress')
        self.assertEqual(l_interface.V4Address, "192.168.1.11", 'Bad V4Address')
        self.assertEqual(l_interface.V6Address, '2000:1D::1, 2000:1D::101', 'Bad V6Address')

    def test_02_ReadAllInterfaces(self):
        l_interfaces = self.m_api._read_interfaces_xml(self.m_xml.interface_sect)
        PrettyPrintAny(l_interfaces, 'All Interfaces')
        PrettyPrintAny(l_interfaces[1], 'Interface_1')
        self.assertEqual(l_interfaces[0].Name, 'eth0', 'Bad Name')
        self.assertEqual(l_interfaces[1].Name, 'wlan0', 'Bad Name')
        self.assertEqual(l_interfaces[2].Name, 'lo', 'Bad Name')
        self.assertEqual(len(l_interfaces), 3, 'Wrong interface count.')

    def test_03_ReadOneNode(self):
        l_node = self.m_api._read_one_node_xml(self.m_xml.node)
        PrettyPrintAny(l_node, 'One Node', 105)
        self.assertEqual(l_node.Name, 'pi-01', 'Bad Name')
        self.assertEqual(l_node.Key, 0, 'Bad Key')
        self.assertEqual(l_node.Active, True, 'Bad Axtive')
        self.assertEqual(l_node.NodeRole, 0, 'Bad NodeRole')

    def test_04_ReadAllNodes(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_nodes, 'All Nodes', 10)
        PrettyPrintAny(l_nodes[0], 'Node 0', 10)

    def test_31_WriteOneInterface(self):
        l_interface = self.m_api._read_one_interface_xml(self.m_xml.interface)
        l_xml = self.m_api._write_one_interface_xml(l_interface)
        PrettyPrintAny(l_xml)

    def test_32_WriteAllInterfaces(self):
        l_interfaces = self.m_api._read_interfaces_xml(self.m_xml.interface_sect)
        l_xml = self.m_api._write_interfaces_xml(l_interfaces)
        PrettyPrintAny(l_xml)

    def test_33_WriteOneNode(self):
        l_node = self.m_api._read_one_node_xml(self.m_xml.node)
        l_xml = self.m_api._write_one_node_xml(l_node)
        PrettyPrintAny(l_xml)

    def test_34_WriteAllNodes(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_nodes_xml(l_nodes)
        PrettyPrintAny(l_xml)


class Test_03_EmptyXML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_EMPTY))

    def test_01_ReadOneInterface(self):
        l_interface = self.m_api._read_one_interface_xml(self.m_xml.interface)
        self.assertEqual(l_interface.Name, 'Missing Name', 'Bad Name')
        PrettyPrintAny(l_interface, 'One empty interface')

    def test_02_ReadAllInterfaces(self):
        l_interfaces = self.m_api._read_interfaces_xml(self.m_xml.interface_sect)
        PrettyPrintAny(l_interfaces, 'All empty interface')
        self.assertEqual(l_interfaces, {}, 'Bad Name')

    def test_03_ReadOneNode(self):
        l_node = self.m_api._read_one_node_xml(self.m_xml.node)
        PrettyPrintAny(l_node, 'One empty node')

    def test_04_ReadAllNodes(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        print('Nodes: {0:}'.format((l_nodes)))
        PrettyPrintAny(l_nodes, 'All empty nodes')

    def test_31_WriteOneInterface(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_nodes_xml(l_nodes)
        PrettyPrintAny(l_xml)

    def test_32_WriteAllInterfaces(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_nodes_xml(l_nodes)
        PrettyPrintAny(l_xml)

    def test_33_WriteOneNodes(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_nodes_xml(l_nodes)
        PrettyPrintAny(l_xml)

    def test_34_WriteAllNodes(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_nodes_xml(l_nodes)
        PrettyPrintAny(l_xml)


class FakeNetiface(object):
    """
    """


class Test_04_Interface(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = node_local.API()

    def test_01_Start(self):
        self.m_api.Start(self.m_pyhouse_obj)


class Test_07_Api(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = node_local.API()

    def test_02_Start(self):
        self.m_api.Start(self.m_pyhouse_obj)

    def test_03_Stop(self):
        self.m_api.Stop()

# ## END DBK
