"""
@name:       PyHouse/src/Modules/Computer/Nodes/test/test_nodes_sync.py
@author:     D. Brian Kimmel
@contact:    d.briankimmel@gmail.com
@copyright:  2016-2016 by D. Brian Kimmel
@date:       Created on Jun 2, 2016
@licencse:   MIT License
@summary:

Passed all 3 tests - DBK - 2016-07-09

"""

__updated__ = '2016-07-09'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData, NodeInterfaceData
from Modules.Computer.Nodes.node_sync import Util
from Modules.Computer.Nodes import nodes_xml
from Modules.Computer.Nodes.nodes_xml import Xml as nodesXml
from Modules.Computer.Nodes.test.xml_nodes import \
        TESTING_NODES_NODE_NAME_0, \
        TESTING_NODES_NODE_UUID_0
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny
from Modules.Utilities import json_tools


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

    def test_02_Data(self):
        self.m_pyhouse_obj.Computer.Nodes = nodes_xml.Xml.read_all_nodes_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer.Nodes, 'PyHouse Computer Nodes'))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer.Nodes[TESTING_NODES_NODE_UUID_0], 'PyHouse Computer Nodes'))
        self.assertEqual(len(self.m_pyhouse_obj.Computer.Nodes), 2)


class C1_Util(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the test
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeData()

    def test_01_Add(self):
        l_node = nodesXml._read_one_node_xml(self.m_xml.node)
        print(PrettyFormatAny.form(l_node, 'Node'))
        l_json = json_tools.encode_json(l_node)
        print(PrettyFormatAny.form(l_json, 'PyHouse'))
        l_msg = json_tools.decode_json_unicode(l_json)
        Util.add_node(self.m_pyhouse_obj, l_msg)
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer.Nodes, 'PyHouse'))
        self.assertNotEqual(self.m_pyhouse_obj.Xml, TESTING_NODES_NODE_NAME_0)

# ## END DBK
