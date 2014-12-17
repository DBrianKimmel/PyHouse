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



class C02_Iface(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_node = NodeData()
        self.m_api = node_local.API()
        self.m_iface_api = node_local.GetAllInterfaceData()

    def test_01_IfaceNames(self):
        l_names = node_local.GetAllInterfaceData()._find_all_interface_names()
        PrettyPrintAny(l_names, 'Names')
        # self.assertEqual()

    def test_02_Node(self):
        l_node = self.m_api.create_local_node()
        PrettyPrintAny(l_node, 'Local Node')
        PrettyPrintAny(l_node.NodeInterfaces[0], 'IFace 0')

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
