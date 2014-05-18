"""
@name: PyHouse/Modules/Core/test/test_node_local.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@note: Created on Apr 29, 2014
@license: MIT License
@summary: This module is for testing local node data.
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, CoreServicesData, NodeData
from Modules.Core import node_local
from Modules.utils import xml_tools
from Modules.test import xml_data

XML = xml_data.XML


class Test_01_XML(unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        self.m_root_element = ET.fromstring(XML)

    def test_0101_read_xml(self):
        l_pyhouse = self.m_root_element
        self.assertEqual(l_pyhouse.tag, 'PyHouse')

    def test_0102_find_nodes(self):
        l_nodes = self.m_root_element.find('Nodes')
        self.assertEqual(l_nodes.tag, 'Nodes')

    def test_0103_find_node_name(self):
        l_nodes = self.m_root_element.find('Nodes')
        l_node = l_nodes.find('Node')
        l_name = l_node.get('Name')
        self.assertEqual(l_name, 'PiNode-1')

    def test_0104_uuid(self):
        l_nodes = self.m_root_element.find('Nodes')
        l_node = l_nodes.find('Node')
        l_uuid = l_node.find('UUID')
        self.assertEqual(l_uuid.text, 'ec955bcf-89c9-11e3-b583-082e5f899999')


class Test_02_ReadXML(unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.XmlRoot = ET.fromstring(XML)
        self.m_pyhouses_obj.CoreServicesData = CoreServicesData()
        self.m_pyhouses_obj.Nodes[0] = NodeData()
        self.m_api = node_local.API()

    def test_0201_read_xml(self):
        self.m_api.read_xml(self.m_pyhouses_obj)


class Test_03_ReadXML(unittest.TestCase):

    def setUp(self):
        self.m_root_element = ET.fromstring(XML)
        self.m_util = xml_tools.PutGetXML()
        self.m_pyhouses_obj = PyHouseData()
        self.m_api = node_local.API()

# ## END DBK
