"""
@name:      PyHouse/src/Modules/Web/test/test_web_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 27, 2015
@Summary:

Passed all 9 tests - DBK - 2015-09-01

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Web.web_xml import Xml as webXml
from Modules.Web.test.xml_web import \
        TESTING_WEB_PORT, \
        TESTING_LOGIN_NAME_0, \
        TESTING_LOGIN_PASSWORD_0, \
        TESTING_LOGIN_ROLE_0, \
        TESTING_LOGIN_FULL_NAME_0, TESTING_LOGIN_KEY_0, TESTING_LOGIN_ACTIVE_0
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = webXml()


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')
        self.assertEqual(self.m_xml.web_sect.tag, 'WebSection')
        # print(PrettyFormatAny.form(self.m_xml.web_sect, 'XML'))

class B1_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Port(self):
        """ Read the web port.
        """
        l_port = webXml._read_port(self.m_xml.web_sect)
        self.assertEqual(l_port, int(TESTING_WEB_PORT))

    def test_02_OneLogin(self):
        """ Read one Login object.
        """
        l_xml = self.m_xml.web_sect.find('LoginSection').find('Login')
        l_obj = webXml._read_one_login(l_xml)
        # print(PrettyFormatAny.form(l_xml, 'XML'))
        # print(PrettyFormatAny.form(l_obj, 'One login'))
        self.assertEqual(l_obj.Name, TESTING_LOGIN_NAME_0)
        self.assertEqual(l_obj.LoginFullName, TESTING_LOGIN_FULL_NAME_0)
        self.assertEqual(l_obj.LoginEncryptedPassword, TESTING_LOGIN_PASSWORD_0)
        self.assertEqual(l_obj.LoginRole, TESTING_LOGIN_ROLE_0)

    def test_03_AllLogins(self):
        """ Read all login objects.
        """
        l_xml = self.m_xml.web_sect.find('LoginSection')
        l_obj = webXml._read_all_logins(l_xml)
        # print(PrettyFormatAny.form(l_xml, 'XML'))
        # print(PrettyFormatAny.form(l_obj, 'One login'))
        self.assertEqual(len(l_obj), 2)

    def test_04_Web(self):
        """ Read all Web info.
        """
        self.m_pyhouse_obj.Computer.Web = webXml.read_web_xml(self.m_pyhouse_obj)
        l_obj = webXml.read_web_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'One login'))
        self.assertEqual(l_obj.WebPort, int(TESTING_WEB_PORT))
        self.assertEqual(len(l_obj.Logins), 2)


class B2_Write(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_web_obj = webXml.read_web_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Web = self.m_web_obj
        self.m_web_xml = ET.Element("WebSection")

    def test_01_Port(self):
        """ Write Web port.
        """
        # print(PrettyFormatAny.form(self.m_web_obj, 'Web'))
        webXml._write_port(self.m_web_obj, self.m_web_xml)
        # print(PrettyFormatAny.form(self.m_web_xml, 'Web'))
        self.assertEqual(self.m_web_xml.find('Port').text, TESTING_WEB_PORT)

    def test_02_OneLogin(self):
        """ Write one Login.
        """
        l_obj = self.m_web_obj.Logins[0]
        # print(PrettyFormatAny.form(l_obj, 'Login Obj'))
        l_xml = webXml._write_one_login(l_obj)
        # print(PrettyFormatAny.form(l_xml, 'Web'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LOGIN_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_LOGIN_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_LOGIN_ACTIVE_0)
        self.assertEqual(l_xml.find('FullName').text, TESTING_LOGIN_FULL_NAME_0)
        self.assertEqual(l_xml.find('Password').text, TESTING_LOGIN_PASSWORD_0)
        self.assertEqual(l_xml.find('Role').text, TESTING_LOGIN_ROLE_0)

    def test_03_AllLogins(self):
        """ Write All logins.
        """
        l_obj = self.m_web_obj.Logins
        l_xml = webXml._write_all_logins(l_obj)
        print(PrettyFormatAny.form(l_xml, 'Web'))
        self.assertEqual(l_xml.find('Login/FullName').text, TESTING_LOGIN_FULL_NAME_0)

    def test_04_Web(self):
        """ Write All logins.
        """
        l_xml = webXml.write_web_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_xml, 'Web'))
        self.assertEqual(l_xml.find('Port').text, TESTING_WEB_PORT)
        self.assertEqual(l_xml.find('LoginSection/Login/FullName').text, TESTING_LOGIN_FULL_NAME_0)

# ## END DBK
