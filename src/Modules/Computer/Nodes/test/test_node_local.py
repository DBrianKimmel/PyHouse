"""
@name:      PyHouse/src/Modules/Core/test/test_node_local.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 29, 2014
@summary:   This module is for testing local node data.

Passed all 19 tests - DBK - 2016-07-08

"""

__updated__ = '2016-07-09'

#  Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

#  Import PyMh files and modules.
from Modules.Core.data_objects import NodeData, NodeInterfaceData
from Modules.Computer.Nodes import nodes_xml
from Modules.Computer.Nodes.node_local import Interfaces, API as localApi
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny


AF_INET = 2


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class FakeNetiface(object):
    """
    """


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the test
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeData()

    def test_01_PyHouseObj(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Xml, 'A1-01-A - PyHouse.Xml'))
        self.assertNotEqual(self.m_pyhouse_obj.Xml, None)

    def test_02_Tags(self):
        # print(PrettyFormatAny.form(self.m_xml, 'A1-02-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')
        self.assertEqual(self.m_xml.node_sect.tag, 'NodeSection')


class A2_Xml(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the test
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeData()

    def test_1_Nodes(self):
        l_xml = self.m_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision').find('NodeSection')
        # print(PrettyFormatAny.form(l_xml, 'A2-1-A - Nodes Xml'))
        self.assertEqual(len(l_xml), 2)

    def test_2_Nodes(self):
        self.m_pyhouse_obj.Computer.Nodes = nodes_xml.Xml.read_all_nodes_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer.Nodes, 'A2-2-A - PyHouse Computer'))
        self.assertEqual(len(self.m_pyhouse_obj.Computer.Nodes), 2)


class A3_Netiface(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the test
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeData()

    def test_01_Families(self):
        """ Check the AF list for what we assume is the correct number later.
        """
        l_fam = Interfaces._list_families()
        # print(PrettyFormatAny.form(l_fam, 'A3-01-A - A_Families', 170))
        self.assertEqual(l_fam[2], 'AF_INET')
        self.assertEqual(l_fam[10], 'AF_INET6')

    def test_02_Gateways(self):
        """ Check the gateways
        """
        l_gate = Interfaces._list_gateways()
        # print(PrettyFormatAny.form(l_gate, 'A3-02-A - Gateways', 170))
        l_v4 = l_gate[2]
        self.assertEqual(l_v4[0][0], '192.168.1.1')

    def test_03_ListInterfaces(self):
        """ Check the interfaces in this computer
        """
        l_int = Interfaces._list_interfaces()
        # print(PrettyFormatAny.form(l_int, 'A3-03-A - Interfaces', 170))
        self.assertEqual(l_int[0], 'lo')

    def test_04_Interfaces(self):
        """ Check the interfaces in this computer
        """
        l_int = Interfaces._list_interfaces()
        # print(PrettyFormatAny.form(l_int, 'A3-04-A - Interface Names', 170))
        for l_name in l_int:
            l_ifa = Interfaces._list_ifaddresses(l_name)
            # print(PrettyFormatAny.form(l_ifa, 'A3-04-B - Interface "{}" Addresses'.format(l_name), 170))
            self.assertGreaterEqual(len(l_ifa), 1)

    def test_05_All(self):
        l_all, _l_v4, _l_v6 = Interfaces._get_all_interfaces()
        for l_ix in l_all:
            # print('{} {}'.format(l_ix, PrettyFormatAny.form(l_all[l_ix], 'A3-05-A - Interface', 170)))
            pass
        # print(PrettyFormatAny.form(l_all, 'A3-05-B - Interfaces', 170))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse'))
        self.assertNotEqual(l_all, None)


class B1_Iface(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_pyhouse_obj.Computer.Nodes = nodes_xml.Xml.read_all_nodes_xml(self.m_pyhouse_obj)
        self.m_node = NodeData()
        self.m_iface_api = Interfaces()

    def test_01_AllIfaceNames(self):
        """ This will be different on different computers

        I don't know how to test the returned list for validity.
        Uncomment the print to see what your computer returned.
        """
        l_names = Interfaces.find_all_interface_names()
        # print(PrettyFormatAny.form(l_names, 'B1-01-A - Names'))
        self.assertGreater(len(l_names), 1)

    def test_02_AddrFamilyName(self):
        """
        We are interested in:
            IPv4 (AF_INET)
            IPv6 (AF_INET6)
            MAC  (AF_LINK)
        """
        # l_ret = Interfaces._find_addr_family_name(17)
        # print(PrettyFormatAny.form(l_ret, 'B1-02 A  Address Lists'))
        # self.assertEqual(l_ret, 'AF_PACKET')
        l_ret = Interfaces._find_addr_family_name(2)
        # print(PrettyFormatAny.form(l_ret, 'B1-02 B Address Lists'))
        self.assertEqual(l_ret, 'AF_INET')
        l_ret = Interfaces._find_addr_family_name(10)
        # print(PrettyFormatAny.form(l_ret, 'B1-02 C Address Lists'))
        self.assertEqual(l_ret, 'AF_INET6')

    def test_03_AddrLists(self):
        """
        I don't know how to test the returned list for validity.
        Uncomment the print to see what your computer returned.
        """
        l_names = Interfaces.find_all_interface_names()
        #  On my laptop: returns 7 interfaces.
        # print(PrettyFormatAny.form(l_names, 'Address Lists'))
        _l_ret = Interfaces._find_addr_lists(l_names[0])
        # print(PrettyFormatAny.form(l_ret, 'Address Lists'))

    def test_04_OneInterfaces(self):
        l_names = Interfaces.find_all_interface_names()
        _l_node = Interfaces._get_one_interface(l_names[1])
        # print(PrettyFormatAny.form(l_node, 'Node Interfaces'))

    def test_05_AllInterfaces(self):
        l_node = NodeData()
        l_if, _l_v4, _l_v6 = Interfaces._get_all_interfaces()
        l_node.NodeInterfaces = l_if
        # print(PrettyFormatAny.form(l_node.NodeInterfaces, 'Node Interfaces'))


class C1_Api(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_1_Api(self):
        _l_api = localApi(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'C1_1_A - PyHouse Computer'))

    def test_2_LoadXml(self):
        l_api = localApi(self.m_pyhouse_obj)
        l_ret = l_api.LoadXml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_ret, 'C1-2-A - PyHouse Computer'))

    def test_3_Start(self):
        #  self.m_api.Start(self.m_pyhouse_obj)
        pass

    def test_4_SaveXml(self):
        l_xml = ET.Element('NodeSection')
        localApi(self.m_pyhouse_obj).SaveXml(l_xml)
        pass

    def test_5_Stop(self):
        localApi(self.m_pyhouse_obj).Stop()
        pass

#  ## END DBK
