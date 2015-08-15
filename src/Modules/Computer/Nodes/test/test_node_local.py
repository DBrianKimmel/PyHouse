"""
@name:      PyHouse/src/Modules/Core/test/test_node_local.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 29, 2014
@summary:   This module is for testing local node data.

Passed all 8 tests - DBK - 2015-08-14

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData, NodeInterfaceData
from Modules.Computer.Nodes import nodes_xml
from Modules.Computer.Nodes.node_local import Interfaces
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        # self.m_api = node_local.API()


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
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse'))
        self.assertNotEqual(self.m_pyhouse_obj.Xml, None)

    def test_02_Data(self):
        self.m_pyhouse_obj.Computer.Nodes = nodes_xml.Xml().read_all_nodes_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'PyHouse Computer'))
        self.assertEqual(len(self.m_pyhouse_obj.Computer.Nodes), 2)


class C02_Iface(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_pyhouse_obj.Computer.Nodes = nodes_xml.Xml().read_all_nodes_xml(self.m_pyhouse_obj)
        self.m_node = NodeData()
        # self.m_api = node_local.API()
        self.m_iface_api = Interfaces()

    def test_01_IfaceNames(self):
        l_names = Interfaces._find_all_interface_names()
        # print(PrettyFormatAny.form(l_names, 'Names'))
        self.assertGreater(len(l_names), 1)

    def test_02_AllInterfaces(self):
        l_node = NodeData()
        l_node = Interfaces.get_all_interfaces(l_node)
        print(PrettyFormatAny.form(l_node.NodeInterfaces, 'Node Interfaces'))

    def test_03_AddrLists(self):
        l_names = Interfaces._find_all_interface_names()
        l_ret = Interfaces._find_addr_lists(l_names[0])
        print(PrettyFormatAny.form(l_ret, 'Address Lists'))
        print(PrettyFormatAny.form(l_ret[23][1], 'Address Lists'))

    def test_04_AddrFamilyName(self):
        l_ret = Interfaces._find_addr_family_name(-1000)
        print(PrettyFormatAny.form(l_ret, 'Address Lists'))
        self.assertEqual(l_ret, 'AF_LINK')
        l_ret = Interfaces._find_addr_family_name(2)
        print(PrettyFormatAny.form(l_ret, 'Address Lists'))
        self.assertEqual(l_ret, 'AF_INET')
        l_ret = Interfaces._find_addr_family_name(23)
        print(PrettyFormatAny.form(l_ret, 'Address Lists'))
        self.assertEqual(l_ret, 'AF_INET6')

    def test_05_GetAddrLists(self):
        l_list = Interfaces._find_all_interface_names()
        l_names = Interfaces._get_address_list(l_list)
        l_ret = Interfaces._find_addr_lists(l_names[0])
        print(PrettyFormatAny.form(l_ret, 'Address Lists'))
        print(PrettyFormatAny.form(l_ret[23][1], 'Address Lists'))


class C07_Api(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        # self.m_api = node_local.API()

    def test_02_Start(self):
        # self.m_api.Start(self.m_pyhouse_obj)
        # PrettyPrintAny(self.m_pyhouse_obj.Computer.Nodes[0], 'Nodes')
        pass

    def test_03_Stop(self):
        # self.m_api.Stop()
        pass

# ## END DBK
