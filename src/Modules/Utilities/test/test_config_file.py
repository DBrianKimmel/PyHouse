"""
@name:      PyHouse/src/Modules/utils/test/test_config_file.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 15, 2014
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Utilities.config_file import ConfigAPI, Util
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A1_XML(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)
        self.m_api = ConfigAPI()

    def test_01_OpenConfig(self):
        l_file = Util._open_config_file(self.m_pyhouse_obj)
        PrettyPrintAny(l_file, 'File')
        PrettyPrintAny(self.m_pyhouse_obj.Xml, 'Xml', 120)
        PrettyPrintAny(self.m_pyhouse_obj.Xml.XmlRoot, 'XmlRoot', 120)

    def test_02_ReadConfig(self):
        Util._open_config_file(self.m_pyhouse_obj)
        l_xml = self.m_pyhouse_obj.Xml.XmlRoot
        l_pyh = self.m_api.read_xml_config_file(self.m_pyhouse_obj)
        PrettyPrintAny(l_pyh, 'XmlData')

    def test_03_Version(self):
        l_pyh = self.m_api.read_xml_config_file(self.m_pyhouse_obj)
        l_ret = self.m_api.get_xml_config_file_version(self.m_pyhouse_obj)
        PrettyPrintAny(l_ret, 'XmlData')

    def test_04_WriteConfig(self):
        Util._open_config_file(self.m_pyhouse_obj)
        l_xml = self.m_pyhouse_obj.Xml.XmlRoot
        self.m_api.write_xml_config_file(self.m_pyhouse_obj, l_xml)
        PrettyPrintAny(l_xml, 'XmlData')

# ## END DBK
