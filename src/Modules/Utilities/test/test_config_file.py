"""
@name: PyHouse/src/Modules/utils/test/test_config_file.py
@author: briank
@contact: D.BrianKimmel@gmail.com>
@Copyright: (c)  2014 by briank
@license: MIT License
@note: Created on Jul 15, 2014
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Utilities import config_file
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_02_XML(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)
        self.m_api = config_file.ConfigAPI()


    def test_0221_ReadConfig(self):
        self.m_api.open_config_file(self.m_pyhouse_obj)
        PrettyPrintAny(self.m_pyhouse_obj.Xml, 'Xml', 120)
        PrettyPrintAny(self.m_pyhouse_obj.Xml.XmlRoot, 'XmlRoot', 120)

    def test_0231_WriteConfig(self):
        self.m_api.open_config_file(self.m_pyhouse_obj)
        l_xml = self.m_pyhouse_obj.Xml.XmlRoot
        l_file = self.m_pyhouse_obj.Xml.XmlFileName
        self.m_api.write_xml_config_file(self.m_pyhouse_obj, l_xml, l_file)

# ## END DBK
