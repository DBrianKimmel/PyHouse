"""
@name: PyHouse/src/Modules/Core/test/test_node_local.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 29, 2014
@summary: This module is for testing local node data.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData, NodeInterfaceData
from Modules.Computer.Nodes import node_local
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


class FakeNetiface(object):
    """
    """


class C01_Structure(SetupMixin, unittest.TestCase):
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
        PrettyPrintAny(self.m_xml.computer_div, 'ComputerDiv XML')
        PrettyPrintAny(self.m_xml.node_sect, 'NodeSect XML')
        PrettyPrintAny(self.m_xml.node, 'Node XML')



class C02_ReadXml(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_OneInterface(self):
        l_interface = self.m_api._read_one_interface_xml(self.m_xml.interface)
        PrettyPrintAny(l_interface, 'One Interface')
        self.assertEqual(l_interface.Name, 'eth0', 'Bad Name')
        self.assertEqual(l_interface.Key, 0, 'Bad Key')
        self.assertEqual(l_interface.Active, True, 'Bad Active')
        self.assertEqual(l_interface.MacAddress, '01:02:03:04:05:06', 'Bad MacAddress')
        self.assertEqual(l_interface.V4Address, "192.168.1.11", 'Bad V4Address')
        self.assertEqual(l_interface.V6Address, '2000:1D::1, 2000:1D::101', 'Bad V6Address')

    def test_02_AllInterfaces(self):
        l_interfaces = self.m_api._read_interfaces_xml(self.m_xml.interface_sect)
        PrettyPrintAny(l_interfaces, 'All Interfaces')
        PrettyPrintAny(l_interfaces[1], 'Interface_1')
        self.assertEqual(l_interfaces[0].Name, 'eth0', 'Bad Name')
        self.assertEqual(l_interfaces[1].Name, 'wlan0', 'Bad Name')
        self.assertEqual(l_interfaces[2].Name, 'lo', 'Bad Name')
        self.assertEqual(len(l_interfaces), 3, 'Wrong interface count.')

    def test_03_OneNode(self):
        l_node = self.m_api._read_one_node_xml(self.m_xml.node)
        PrettyPrintAny(l_node, 'One Node', 105)
        self.assertEqual(l_node.Name, 'pi-01', 'Bad Name')
        self.assertEqual(l_node.Key, 0, 'Bad Key')
        self.assertEqual(l_node.Active, True, 'Bad Active')
        self.assertEqual(l_node.NodeRole, 0, 'Bad NodeRole')

    def test_04_AllNodes(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_nodes, 'All Nodes', 10)
        PrettyPrintAny(l_nodes[0], 'Node 0', 10)



class C03_Write(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_OneInterface(self):
        l_interface = self.m_api._read_one_interface_xml(self.m_xml.interface)
        l_xml = self.m_api._write_one_interface_xml(l_interface)
        PrettyPrintAny(l_xml)
        self.assertEqual(l_xml.attrib['Name'], 'eth0')
        self.assertEqual(l_xml.attrib['Key'], '0')
        self.assertEqual(l_xml.attrib['Active'], 'True')

    def test_02_AllInterfaces(self):
        l_interfaces = self.m_api._read_interfaces_xml(self.m_xml.interface_sect)
        l_xml = self.m_api._write_interfaces_xml(l_interfaces)
        PrettyPrintAny(l_xml)

    def test_03_OneNode(self):
        l_node = self.m_api._read_one_node_xml(self.m_xml.node)
        l_xml = self.m_api._write_one_node_xml(l_node)
        PrettyPrintAny(l_xml)
        self.assertEqual(l_xml.attrib['Name'], 'pi-01')
        self.assertEqual(l_xml.attrib['Key'], '0')
        self.assertEqual(l_xml.attrib['Active'], 'True')

    def test_04_AllNodes(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_nodes_xml(l_nodes)
        PrettyPrintAny(l_xml)



class C04_ReadEmptyXML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_EMPTY))

    def test_01_OneInterface(self):
        l_interface = self.m_api._read_one_interface_xml(self.m_xml.interface)
        self.assertEqual(l_interface.Name, 'Missing Name', 'Bad Name')
        PrettyPrintAny(l_interface, 'One empty interface')

    def test_02_AllInterfaces(self):
        l_interfaces = self.m_api._read_interfaces_xml(self.m_xml.interface_sect)
        PrettyPrintAny(l_interfaces, 'All empty interface')
        self.assertEqual(l_interfaces, {}, 'Bad Name')

    def test_03_OneNode(self):
        l_node = self.m_api._read_one_node_xml(self.m_xml.node)
        PrettyPrintAny(l_node, 'One empty node')

    def test_04_AllNodes(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        print('Nodes: {0:}'.format((l_nodes)))
        PrettyPrintAny(l_nodes, 'All empty nodes')



class C05_WriteEmptyXML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_EMPTY))

    def test_01_OneInterface(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_nodes_xml(l_nodes)
        PrettyPrintAny(l_xml)

    def test_02_AllInterfaces(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_nodes_xml(l_nodes)
        PrettyPrintAny(l_xml)

    def test_03_OneNode(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_nodes_xml(l_nodes)
        PrettyPrintAny(l_xml)

    def test_04_AllNodes(self):
        l_nodes = self.m_api.read_all_nodes_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_nodes_xml(l_nodes)
        PrettyPrintAny(l_xml)



class C06_Interface(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_node = NodeData()
        self.m_api = node_local.API()
        self.m_iface_api = node_local.GetAllInterfaceData()

    def test_01_IfaceNames(self):
        l_names = node_local.GetAllInterfaceData()._find_all_interface_names()
        PrettyPrintAny(l_names, 'Names')

    def test_02_Node(self):
        l_node = self.m_api.create_local_node()
        PrettyPrintAny(l_node, 'Local Node')

    def test_03_Node(self):
        pass

    def test_04_Node(self):
        pass



class C07_Api(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = node_local.API()

    def test_02_Start(self):
        self.m_api.Start(self.m_pyhouse_obj)
        PrettyPrintAny(self.m_pyhouse_obj.Computer.Nodes[0], 'Nodes')

    def test_03_Stop(self):
        self.m_api.Stop()

# ## END DBK
