"""
@name:      PyHouse/src/Modules/Computer/Nodes/test/test_nodes_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 15, 2014
@Summary:

Passed all 15 tests - DBK - 2018-02-12

"""

__updated__ = '2019-07-05'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from Modules.Core.data_objects import NodeInformation, NodeInterfaceData
from Modules.Computer.Nodes.nodes_xml import Xml as nodesXml
from Modules.Computer.Nodes.test.xml_nodes import \
        TESTING_NODES_NODE_NAME_0, \
        TESTING_NODES_NODE_NAME_1, \
        TESTING_NODES_NODE_KEY_0, \
        TESTING_NODES_NODE_KEY_1, \
        TESTING_NODES_NODE_ACTIVE_0, \
        TESTING_NODES_NODE_ACTIVE_1, \
        TESTING_NODES_NODE_UUID_0, \
        TESTING_NODES_NODE_UUID_1, \
        TESTING_NODES_INTERFACE_NAME_0_0, \
        TESTING_NODES_INTERFACE_KEY_0_0, \
        TESTING_NODES_INTERFACE_ACTIVE_0_0, \
        TESTING_NODES_INTERFACE_MAC_ADDRESS_0_0, \
        TESTING_NODES_INTERFACE_ADDRESS_V4_0_0, \
        TESTING_NODES_INTERFACE_ADDRESS_V6_0_0, \
        TESTING_NODES_INTERFACE_NAME_0_1, \
        TESTING_NODES_INTERFACE_KEY_0_1, \
        TESTING_NODES_INTERFACE_ACTIVE_0_1, \
        TESTING_NODES_INTERFACE_NAME_0_2, \
        TESTING_NODES_INTERFACE_KEY_0_2, \
        TESTING_NODES_INTERFACE_ACTIVE_0_2, \
        TESTING_NODES_INTERFACE_UUID_0_0, \
        TESTING_NODES_INTERFACE_UUID_0_1, \
        TESTING_NODES_INTERFACE_UUID_0_2, \
        TESTING_NODES_INTERFACE_MAC_ADDRESS_0_1, \
        TESTING_NODES_INTERFACE_ADDRESS_V4_0_1, \
        TESTING_NODES_INTERFACE_ADDRESS_V6_0_1, \
        TESTING_NODES_INTERFACE_MAC_ADDRESS_0_2, \
        TESTING_NODES_INTERFACE_ADDRESS_V4_0_2, \
        TESTING_NODES_INTERFACE_ADDRESS_V6_0_2, \
        TESTING_NODES_CONNECTION_ADDRESS_V4_0, \
        TESTING_NODES_CONNECTION_ADDRESS_V6_0, \
        TESTING_NODES_INTERFACE_TYPE_0_0, \
        TESTING_NODES_NODE_ROLL_0, \
        TESTING_NODES_NODE_ROLL_1, \
        XML_NODES, \
        TESTING_NODE_SECTION, TESTING_NODES_INTERFACE_COMMENT_0_0, TESTING_NODES_NODE_COMMENT_0, TESTING_NODES_INTERFACE_LAST_UPDATE_0_0
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

DIVISION = 'ComputerDivision'
NODE_SECTION = 'NodeSection'


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


class A0(unittest.TestCase):

    def test_00_Print(self):
        print('Id: test_nodes_xml')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeInformation()

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        Test some scattered things so we don't end up with hundreds of asserts.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Xml'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, DIVISION)

    def test_02_Computer(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'A1-02-A - PyHouse'))
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))

    def test_01_Raw(self):
        l_raw = XML_NODES
        # print('A2-01-A - Raw', l_raw)
        self.assertEqual(l_raw[:13], '<NodeSection>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_NODES)
        print('A2-02-A - Parsed', PrettyFormatAny.form(l_xml, 'A2-02-A Parsed'))
        self.assertEqual(l_xml.tag, TESTING_NODE_SECTION)


class A3_Xml(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeInformation()

    def test_01_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        Test some scattered things so we don't end up with hundreds of asserts.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Xml'))


class B1_Read(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_OneInterface0(self):
        """ Test that the entire NodeInterface() obj is built properly
        """
        l_interface = nodesXml._read_one_interface_xml(self.m_xml.interface)
        print(PrettyFormatAny.form(l_interface, 'B1-01-A - Interface'))
        self.assertEqual(l_interface.Name, TESTING_NODES_INTERFACE_NAME_0_0)
        self.assertEqual(l_interface.Key, int(TESTING_NODES_INTERFACE_KEY_0_0))
        self.assertEqual(l_interface.Active, bool(TESTING_NODES_INTERFACE_ACTIVE_0_0))
        self.assertEqual(l_interface.UUID, TESTING_NODES_INTERFACE_UUID_0_0)
        self.assertEqual(l_interface.Comment, TESTING_NODES_INTERFACE_COMMENT_0_0)
        self.assertEqual(str(l_interface.LastUpdate), TESTING_NODES_INTERFACE_LAST_UPDATE_0_0)
        self.assertEqual(l_interface.NodeInterfaceType, TESTING_NODES_INTERFACE_TYPE_0_0)
        self.assertEqual(l_interface.MacAddress, TESTING_NODES_INTERFACE_MAC_ADDRESS_0_0)
        self.assertEqual(l_interface.V4Address, TESTING_NODES_INTERFACE_ADDRESS_V4_0_0)
        self.assertEqual(l_interface.V6Address, TESTING_NODES_INTERFACE_ADDRESS_V6_0_0)

    def test_02_AllInterfaces(self):
        l_interfaces = nodesXml._read_interfaces_xml(self.m_xml.interface_sect)
        print(PrettyFormatAny.form(l_interfaces, 'B1-02-A - Interfaces'))
        self.assertEqual(len(l_interfaces), 3)
        self.assertEqual(l_interfaces[0].Name, TESTING_NODES_INTERFACE_NAME_0_0)
        self.assertEqual(l_interfaces[1].Name, TESTING_NODES_INTERFACE_NAME_0_1)
        self.assertEqual(l_interfaces[2].Name, TESTING_NODES_INTERFACE_NAME_0_2)

    def test_03_Node_0(self):
        l_node = nodesXml._read_one_node_xml(self.m_xml.node)
        print(PrettyFormatAny.form(l_node, 'B1-03-A - One Node', 108))
        print(PrettyFormatAny.form(l_node.NodeInterfaces, 'B1-03-B - One Node', 108))
        print(PrettyFormatAny.form(l_node.NodeInterfaces[1], 'B1-03-B - One Node', 108))
        self.assertEqual(l_node.Name, TESTING_NODES_NODE_NAME_0)
        self.assertEqual(l_node.Key, int(TESTING_NODES_NODE_KEY_0))
        self.assertEqual(l_node.Active, bool(TESTING_NODES_NODE_ACTIVE_0))
        self.assertEqual(l_node.UUID, (TESTING_NODES_NODE_UUID_0))
        self.assertEqual(l_node.Comment, (TESTING_NODES_NODE_COMMENT_0))
        self.assertEqual(l_node.NodeRole, int(TESTING_NODES_NODE_ROLL_0))

    def test_04_Node_1(self):
        l_ix = self.m_xml.node_sect[1]
        print(PrettyFormatAny.form(l_ix, 'B1-04-A One Node XML'))
        l_node = nodesXml._read_one_node_xml(l_ix)
        print(PrettyFormatAny.form(l_node, 'B1-04-B One Node', 108))
        self.assertEqual(l_node.Name, TESTING_NODES_NODE_NAME_1)
        self.assertEqual(l_node.Key, int(TESTING_NODES_NODE_KEY_1))
        self.assertEqual(l_node.Active, bool(TESTING_NODES_NODE_ACTIVE_1))
        self.assertEqual(l_node.NodeRole, int(TESTING_NODES_NODE_ROLL_1))

    def test_05_AllNodes(self):
        l_nodes = nodesXml.read_all_nodes_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_nodes, 'B1-05-A - All Nodes', 108))
        self.assertEqual(len(l_nodes), 2)
        self.assertEqual(l_nodes[TESTING_NODES_NODE_UUID_0].Name, TESTING_NODES_NODE_NAME_0)
        self.assertEqual(l_nodes[TESTING_NODES_NODE_UUID_1].Name, TESTING_NODES_NODE_NAME_1)


class C1_Write(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_OneInterface(self):
        l_interface = nodesXml._read_one_interface_xml(self.m_xml.interface)
        l_xml = nodesXml._write_one_interface_xml(l_interface)
        print(PrettyFormatAny.form(l_xml, 'C1-01-A -  One Interface'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_NODES_INTERFACE_NAME_0_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_NODES_INTERFACE_KEY_0_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_NODES_INTERFACE_ACTIVE_0_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_NODES_INTERFACE_UUID_0_0)
        self.assertEqual(l_xml.find('InterfaceType').text, TESTING_NODES_INTERFACE_TYPE_0_0)
        self.assertEqual(l_xml.find('MacAddress').text, TESTING_NODES_INTERFACE_MAC_ADDRESS_0_0)
        self.assertEqual(l_xml.find('IPv4Address').text, TESTING_NODES_INTERFACE_ADDRESS_V4_0_0)
        self.assertEqual(l_xml.find('IPv6Address').text, TESTING_NODES_INTERFACE_ADDRESS_V6_0_0)

    def test_02_AllInterfaces(self):
        l_interfaces = nodesXml._read_interfaces_xml(self.m_xml.interface_sect)
        l_xml = nodesXml._write_interfaces_xml(l_interfaces)
        print(PrettyFormatAny.form(l_xml, 'C1-02-A - All Interfaces'))
        self.assertEqual(l_xml[0].attrib['Name'], TESTING_NODES_INTERFACE_NAME_0_0)
        self.assertEqual(l_xml[0].attrib['Key'], TESTING_NODES_INTERFACE_KEY_0_0)
        self.assertEqual(l_xml[0].attrib['Active'], TESTING_NODES_INTERFACE_ACTIVE_0_0)
        self.assertEqual(l_xml[0].find('UUID').text, TESTING_NODES_INTERFACE_UUID_0_0)
        self.assertEqual(l_xml[0].find('MacAddress').text, TESTING_NODES_INTERFACE_MAC_ADDRESS_0_0)
        # self.assertEqual(l_xml[0][2].text, TESTING_NODES_INTERFACE_ADDRESS_V4_0_0)
        # self.assertEqual(l_xml[0][3].text, TESTING_NODES_INTERFACE_ADDRESS_V6_0_0)
        self.assertEqual(l_xml[1].attrib['Name'], TESTING_NODES_INTERFACE_NAME_0_1)
        self.assertEqual(l_xml[1].attrib['Key'], TESTING_NODES_INTERFACE_KEY_0_1)
        self.assertEqual(l_xml[1].attrib['Active'], TESTING_NODES_INTERFACE_ACTIVE_0_1)
        self.assertEqual(l_xml[1].find('UUID').text, TESTING_NODES_INTERFACE_UUID_0_1)
        self.assertEqual(l_xml[1].find('MacAddress').text, TESTING_NODES_INTERFACE_MAC_ADDRESS_0_1)
        # self.assertEqual(l_xml[1][2].text, TESTING_NODES_INTERFACE_ADDRESS_V4_0_1)
        # self.assertEqual(l_xml[1][3].text, TESTING_NODES_INTERFACE_ADDRESS_V6_0_1)
        self.assertEqual(l_xml[2].attrib['Name'], TESTING_NODES_INTERFACE_NAME_0_2)
        self.assertEqual(l_xml[2].attrib['Key'], TESTING_NODES_INTERFACE_KEY_0_2)
        self.assertEqual(l_xml[2].attrib['Active'], TESTING_NODES_INTERFACE_ACTIVE_0_2)
        self.assertEqual(l_xml[2].find('UUID').text, TESTING_NODES_INTERFACE_UUID_0_2)
        self.assertEqual(l_xml[2].find('MacAddress').text, TESTING_NODES_INTERFACE_MAC_ADDRESS_0_2)
        # self.assertEqual(l_xml[2][2].text, TESTING_NODES_INTERFACE_ADDRESS_V4_0_2)
        # self.assertEqual(l_xml[2][3].text, TESTING_NODES_INTERFACE_ADDRESS_V6_0_2)

    def test_03_OneNode(self):
        l_node = nodesXml._read_one_node_xml(self.m_xml.node)
        l_xml = nodesXml._write_one_node_xml(l_node)
        print(PrettyFormatAny.form(l_xml, 'C1-03-A - One Node'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_NODES_NODE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_NODES_NODE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_NODES_NODE_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_NODES_NODE_UUID_0)
        # self.assertEqual(l_xml[1].text, TESTING_NODES_CONNECTION_ADDRESS_V4_0)
        # self.assertEqual(l_xml[2].text, TESTING_NODES_CONNECTION_ADDRESS_V6_0)
        self.assertEqual(l_xml.find('NodeRole').text, TESTING_NODES_NODE_ROLL_0)

    def test_04_AllNodes(self):
        l_nodes = nodesXml.read_all_nodes_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_nodes, 'C1-04-A All Nodes'))
        self.m_pyhouse_obj.Computer.Nodes = l_nodes
        l_xml, l_count = nodesXml.write_nodes_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_xml, 'C1-04-B All Nodes'))
        self.assertEqual(l_count, 2)
        # self.assertEqual(l_xml[0].attrib['Name'], TESTING_NODES_NODE_NAME_0)
        # self.assertEqual(l_xml[1].attrib['Name'], TESTING_NODES_NODE_NAME_1)

# ## END DBK
