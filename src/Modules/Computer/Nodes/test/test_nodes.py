"""
@name:      PyHouse/src/Modules/Computer/Nodes/test/test_nodes.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep 15, 2015
@Summary:

Passed all 6 tests - DBK - 2016-06-07

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData, NodeInterfaceData
from Modules.Computer.Nodes.nodes import API as nodesApi
from Modules.Computer.Nodes.node_local import API as localApi
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny
from Modules.Computer.Nodes.test.xml_nodes import TESTING_NODES_NODE_NAME_0


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the test
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeData()

    def test_01_PyHouse(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse'))
        self.assertNotEqual(self.m_pyhouse_obj.Xml, None)


class B1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the test
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeData()

    def test_01_PyHouse(self):
        nodesApi(self.m_pyhouse_obj).LoadXml(self.m_pyhouse_obj)
        l_nodes = self.m_pyhouse_obj.Computer.Nodes
        # print(PrettyFormatAny.form(l_nodes, 'PyHouse'))
        # print(PrettyFormatAny.form(l_nodes[TESTING_NODES_NODE_NAME_0], 'PyHouse'))
        self.assertEqual(l_nodes[TESTING_NODES_NODE_NAME_0].Name, TESTING_NODES_NODE_NAME_0)


class C1_Api(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_init(self):
        _l_api = localApi(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'PyHouse Computer'))

    def test_02_LoadXml(self):
        l_api = localApi(self.m_pyhouse_obj)
        l_ret = l_api.LoadXml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_ret, 'PyHouse Computer'))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'PyHouse Computer'))

    def test_02_Start(self):
        #  self.m_api.Start(self.m_pyhouse_obj)
        pass

    def test_03_Stop(self):
        #  self.m_api.Stop()
        pass

# ## END DBK
