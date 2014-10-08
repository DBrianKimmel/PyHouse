"""
@name: PyHouse/src/test/test_testing_mixin.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Oct 6, 2014
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Utilities.tools import PrettyPrintAny
from test import xml_data
from test.testing_mixin import SetupPyHouseObj


class C01_Build(unittest.TestCase):
    """ This section tests the reading and writing of XML used by inernet.
    """

    def setUp(self):
        self.m_api = SetupPyHouseObj()

    def test_01_Computer(self):
        l_config = self.m_api._BuildComputer()
        PrettyPrintAny(l_config, 'Config')
        self.assertDictEqual(l_config.Email, {})
        self.assertDictEqual(l_config.InternetConnection, {})
        self.assertDictEqual(l_config.Nodes, {})
        self.assertDictEqual(l_config.Web, {})

    def test_02_House(self):
        l_config = self.m_api._BuildHouse()
        PrettyPrintAny(l_config, 'Config')
        self.assertEqual(l_config.Key, 0)

    def test_03_PyHouse(self):
        l_root = None
        l_config = self.m_api.BuildPyHouseObj(l_root)
        PrettyPrintAny(l_config, 'Config')

    def test_04_Root(self):
        l_root = ET.fromstring(xml_data.XML_LONG)
        PrettyPrintAny(l_root)

    def test_05_XML(self):
        l_root = ET.fromstring(xml_data.XML_LONG)
        l_config = self.m_api.BuildXml(l_root)
        PrettyPrintAny(l_config, 'Config')

# ## END DBK
