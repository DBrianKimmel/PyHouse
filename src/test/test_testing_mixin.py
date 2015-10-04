"""
@name:      PyHouse/src/test/test_testing_mixin.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Oct 6, 2014
@Summary:

Passed all 7 tests - DBK - 2015-08-01

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A1_Setup(SetupMixin, unittest.TestCase):
    """ This section tests the SetupMixin Class
    """

    def setUp(self):
        # SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        pass

    def test_01_RawXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        print(XML_LONG)

    def test_02_XML(self):
        """ Be sure that the XML contains the right stuff.
        """
        print(PrettyFormatAny.form(XML_LONG, 'XML', 90))


class C01_Build(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by inernet.
    """

    def setUp(self):
        self.m_api = SetupPyHouseObj()

    def test_01_Computer(self):
        l_config = self.m_api._build_computer()
        print(PrettyFormatAny.form(l_config, 'Config'))
        # self.assertDictEqual(l_config.Email, {})
        # self.assertDictEqual(l_config.InternetConnection, {})
        # self.assertDictEqual(l_config.Nodes, {})
        # self.assertDictEqual(l_config.Web, {})

    def test_02_House(self):
        l_obj = {}
        l_config = self.m_api._build_house(l_obj)
        print(PrettyFormatAny.form(l_config, 'Config'))
        self.assertEqual(l_config.Key, 0)

    def test_03_PyHouse(self):
        l_root = None
        l_config = self.m_api.BuildPyHouseObj(l_root)
        print(PrettyFormatAny.form(l_config, 'Config'))

    def test_04_Root(self):
        l_root = ET.fromstring(XML_LONG)
        print(PrettyFormatAny.form(l_root))

    def test_05_XML(self):
        l_root = ET.fromstring(XML_LONG)
        l_config = self.m_api.BuildXml(l_root)
        print(PrettyFormatAny.form(l_config, 'Config'))

# ## END DBK
