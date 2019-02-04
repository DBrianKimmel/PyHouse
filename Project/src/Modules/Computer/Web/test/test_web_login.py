"""
@name:      PyHouse/src/Modules/Computer/Web/test/test_web_login.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 29, 2014
@Summary:

Passed all 8 tests - DBK - 2017-01-11

"""

__updated__ = '2019-02-03'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Computer.Nodes.nodes_xml import Xml as nodesXml
from Modules.Computer.Web.web_xml import Xml as webXml
from Modules.Computer.Web import web_login
from Modules.Families import VALID_FAMILIES
from Modules.Computer.Web.test.xml_web import TESTING_LOGIN_NAME_0, TESTING_WEB_PORT
from Modules.Computer.Web.web import WorkspaceData
from Modules.Core.Utilities import json_tools
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_web_login')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the above setup for things we will need further down in the tests.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Tags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')
        self.assertEqual(self.m_xml.web_sect.tag, 'WebSection')


class A2_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Port(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_xml = self.m_xml.web_sect
        # print(PrettyFormatAny.form(l_xml, 'A2-01-A - XML'))
        self.assertEqual(l_xml.find('Port').text, TESTING_WEB_PORT)

    def test_02_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml.web_sect, 'A2-02-A - Web Xml'))

    def test_03_ReadXML(self):
        l_web = webXml.read_web_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Web = l_web
        # print(PrettyFormatAny.form(l_web, 'A2-03-A - Web Data'))
        self.assertEqual(l_web.WebPort, 8580)
        self.assertEqual(len(l_web.Logins), 2)
        self.assertEqual(l_web.Logins[0].Name, TESTING_LOGIN_NAME_0)

    def test_04_WriteXML(self):
        l_web = webXml.read_web_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Web = l_web
        # print(PrettyFormatAny.form(l_web, 'A2-04-A - Web Data'))
        l_xml = webXml.write_web_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'A2-04-B - XML'))
        pass


class C1_Element(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        l_web = webXml.read_web_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Web = l_web
        l_nodes = nodesXml.read_all_nodes_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Nodes = l_nodes
        self.m_worksapce = WorkspaceData
        self.m_worksapce.m_pyhouse_obj = self.m_pyhouse_obj

    def test_01_DoLogin(self):
        pass

    def test_02_ValidList(self):
        l_json = web_login.LoginElement(self.m_worksapce).getValidLists()
        l_test = json_tools.decode_json_unicode(l_json)
        # print(PrettyFormatAny.form(l_test, 'C1-02-A - JSON', 40))
        self.assertEqual(l_test['Families'], VALID_FAMILIES)

# ## END DBK
