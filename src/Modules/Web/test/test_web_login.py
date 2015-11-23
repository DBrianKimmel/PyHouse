"""
@name:      PyHouse/src/Modules/Web/test/test_web_login.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 29, 2014
@Summary:

Passed 3 of 4 tests - DBK - 2015-11-16

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Computer.Nodes.nodes_xml import Xml as nodesXml
from Modules.Web.web_xml import Xml as webXml
from Modules.Web import web_login
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny
from Modules.Web.test.xml_web import TESTING_LOGIN_NAME_0
from Modules.Web.web import WorkspaceData
from Modules.Computer.Nodes.test.xml_nodes import TESTING_NODES_NODE_NAME_0
from Modules.Utilities import json_tools


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A2_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        print(PrettyFormatAny.form(self.m_xml.web_sect, 'Web Xml'))
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.web_sect.tag, 'WebSection')

    def test_02_ReadXML(self):
        l_web = webXml.read_web_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Web = l_web
        # print(PrettyFormatAny.form(l_web, 'Web Data'))
        self.assertEqual(l_web.WebPort, 8580)
        self.assertEqual(len(l_web.Logins), 2)
        self.assertEqual(l_web.Logins[0].Name, TESTING_LOGIN_NAME_0)

    def test_03_WriteXML(self):
        l_web = webXml.read_web_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Web = l_web
        print(PrettyFormatAny.form(l_web, 'Web Data'))
        l_xml = webXml.write_web_xml(l_web)
        print(PrettyFormatAny.form(l_xml, 'XML'))


class C02_Element(SetupMixin, unittest.TestCase):

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
        print(PrettyFormatAny.form(l_test, 'JSON', 40))
        self.assertEqual(l_test['ServerName'], TESTING_NODES_NODE_NAME_0)

# ## END DBK
