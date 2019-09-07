"""
@name:      PyHouse/src/Modules/Computer/Nodes/_test/test_nodes.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep 15, 2015
@Summary:

Passed all 8 tests - DBK - 2019-01-19

"""

__updated__ = '2019-07-05'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import NodeInformation, NodeInterfaceData
from Modules.Computer.Nodes.nodes import API as nodesApi
from Modules.Computer.Nodes.node_local import API as localApi
from Modules.Computer.Nodes.test.xml_nodes import \
    TESTING_NODES_NODE_NAME_0, \
    TESTING_NODES_NODE_UUID_0
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_nodes')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the _test
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeInformation()

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Xml'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')
        self.assertEqual(self.m_xml.node_sect.tag, 'NodeSection')
        self.assertEqual(self.m_xml.node.tag, 'Node')


class A2_Xml(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeInformation()

    def test_01_Nodes(self):
        l_xml = self.m_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision').find('NodeSection')
        # print(PrettyFormatAny.form(l_xml, 'A2-01-A - Nodes Xml'))
        self.assertEqual(len(l_xml), 2)


class B1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the _test
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeInformation()

    def test_01_PyHouse(self):
        nodesApi(self.m_pyhouse_obj).LoadXml(self.m_pyhouse_obj)
        l_nodes = self.m_pyhouse_obj.Computer.Nodes
        # print(PrettyFormatAny.form(l_nodes, 'B1-01-A - Nodes'))
        # print(PrettyFormatAny.form(l_nodes[TESTING_NODES_NODE_UUID_0], 'B1-01-B - PyHouse'))
        self.assertEqual(l_nodes[TESTING_NODES_NODE_UUID_0].Name, TESTING_NODES_NODE_NAME_0)
        pass


class C1_Api(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_init(self):
        _l_api = localApi(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'PyHouse Computer'))
        pass

    def test_02_LoadXml(self):
        l_api = localApi(self.m_pyhouse_obj)
        _l_ret = l_api.LoadXml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_ret, 'PyHouse Computer'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'PyHouse Computer'))
        pass

    def test_02_Start(self):
        #  self.m_api.Start(self.m_pyhouse_obj)
        pass

    def test_03_Stop(self):
        #  self.m_api.Stop()
        pass

# ## END DBK
