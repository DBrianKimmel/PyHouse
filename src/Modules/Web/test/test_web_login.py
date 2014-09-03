"""
@name: PyHouse/src/Modules/Web/test/test_web_login.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com>
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Aug 29, 2014
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from twisted.internet.defer import succeed
from twisted.web import server
from twisted.web.test.test_web import DummyRequest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, ComputerInformation, XmlInformation
from Modules.Web import web_login
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_02_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_0201_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.web_sect.tag, 'WebSection', 'XML - No Web section')
        PrettyPrintAny(self.m_xml.web_sect, 'Web Xml')

    def test_0211_ReadXML(self):
        l_web = self.m_api.read_web_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Logs = l_web
        PrettyPrintAny(l_web, 'Web Data')
        self.assertEqual(l_web.WebPort, 8580, 'Bad WebPort')

    def test_0221_WriteXML(self):
        l_web = self.m_api.read_web_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_web_xml(l_web)
        PrettyPrintAny(l_xml)


class Test_03(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_0301_DoLogin(self):
        pass

# ## END DBK
