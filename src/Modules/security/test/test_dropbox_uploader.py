"""
@name: PyHouse/src/Modules/security/test/test_dropbox_uploader.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@note: Created on May 31, 2014
@license: MIT License
@summary: Test uploading files to dropbox.

"""


# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, CoreServices, NodeData
from Modules.Core import node_local
# from Modules.utils import xml_tools
from src.test import xml_data


class Test_01_XML(unittest.TestCase):


    def setUp(self):
        self.m_root_element = ET.fromstring(xml_data.XML_LONG)

    def test_0101_read_xml(self):
        l_pyhouse = self.m_root_element
        self.assertEqual(l_pyhouse.tag, 'PyHouse')


class Test_02_ReadXML(unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.XmlRoot = ET.fromstring(xml_data.XML_LONG)
        self.m_pyhouse_obj.CoreServicesData = CoreServices()
        self.m_pyhouse_obj.Nodes[0] = NodeData()
        self.m_api = node_local.API()


class Test_03_Connect(unittest.TestCase):

    def SetUp(self):
        pass

    def test_0301_connect(self):
        pass


class Test_06_DropboxConnect(unittest.TestCase):

    def SetUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.XmlRoot = ET.fromstring(xml_data.XML_LONG)

    def test_0601_connect(self):
        pass

# ## END DBK
