"""
@name:      PyHouse/src/Modules/Computer/Web/test/test_web_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 27, 2015
@Summary:

Passed all 14 tests - DBK - 2018-01-27

"""

__updated__ = '2018-01-27'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import WebData, LoginData
from Modules.Computer.Web.web_xml import Xml as webXml
from Modules.Computer.test.xml_computer import TESTING_COMPUTER_DIVISION
from Modules.Computer.Web.test.xml_web import \
    TESTING_WEB_PORT, \
    TESTING_LOGIN_NAME_0, \
    TESTING_LOGIN_PASSWORD_0, \
    TESTING_LOGIN_ROLE_0, \
    TESTING_LOGIN_FULL_NAME_0, \
    TESTING_LOGIN_KEY_0, \
    TESTING_LOGIN_ACTIVE_0, \
    TESTING_WEB_SECURE_PORT, \
    TESTING_WEB_SECTION, \
    TESTING_LOGIN_SECTION, \
    XML_WEB_SERVER, \
    TESTING_LOGIN_UUID_0, \
    TESTING_LOGIN_NAME_1, \
    TESTING_LOGIN_KEY_1, \
    TESTING_LOGIN_ACTIVE_1, \
    TESTING_LOGIN_UUID_1, \
    TESTING_LOGIN_FULL_NAME_1, \
    TESTING_LOGIN_PASSWORD_1, \
    TESTING_LOGIN_ROLE_1, \
    TESTING_WEB_SOCKET_PORT
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_pyhouse_obj.Computer.Web = WebData()
        self.m_pyhouse_obj.Computer.Web.Logins = LoginData()
        self.m_api = webXml()


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_web_xml')


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, TESTING_COMPUTER_DIVISION)
        self.assertEqual(self.m_xml.web_sect.tag, TESTING_WEB_SECTION)
        self.assertEqual(self.m_xml.login_sect.tag, TESTING_LOGIN_SECTION)

    def test_02_LoginSection(self):
        self.assertEqual(self.m_xml.login_sect.tag, 'LoginSection')
        print(PrettyFormatAny.form(self.m_xml.login_sect, 'A1-03-A - XML'))


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_WEB_SERVER
        # print(l_raw)
        self.assertEqual(l_raw[:12], '<WebSection>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_WEB_SERVER)
        # print(l_xml)
        self.assertEqual(l_xml.tag, TESTING_WEB_SECTION)


class B1_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Ports(self):
        """ Read the web ports.
        """
        l_port, l_secure, l_socket = webXml._read_ports(self.m_xml.web_sect)
        self.assertEqual(str(l_port), TESTING_WEB_PORT)
        self.assertEqual(str(l_secure), TESTING_WEB_SECURE_PORT)
        self.assertEqual(str(l_socket), TESTING_WEB_SOCKET_PORT)

    def test_02_Login_0(self):
        """ Read one Login object.
        """
        l_xml = self.m_xml.login_sect[0]
        l_obj = webXml._read_one_login(l_xml)
        # print(PrettyFormatAny.form(l_xml, 'B1-02-A - XML'))
        # print(PrettyFormatAny.form(l_obj, 'B1-02-B - One login'))
        self.assertEqual(l_obj.Name, TESTING_LOGIN_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_LOGIN_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_LOGIN_ACTIVE_0)
        self.assertEqual(str(l_obj.UUID), TESTING_LOGIN_UUID_0)
        self.assertEqual(l_obj.LoginFullName, TESTING_LOGIN_FULL_NAME_0)
        self.assertEqual(l_obj.LoginPasswordCurrent, TESTING_LOGIN_PASSWORD_0)
        self.assertEqual(l_obj.LoginRole, TESTING_LOGIN_ROLE_0)

    def test_03_Login_1(self):
        """ Read one Login object.
        """
        l_xml = self.m_xml.login_sect[1]
        l_obj = webXml._read_one_login(l_xml)
        # print(PrettyFormatAny.form(l_xml, 'B1-03-A - XML'))
        # print(PrettyFormatAny.form(l_obj, 'B1-03-B - One login'))
        self.assertEqual(l_obj.Name, TESTING_LOGIN_NAME_1)
        self.assertEqual(str(l_obj.Key), TESTING_LOGIN_KEY_1)
        self.assertEqual(str(l_obj.Active), TESTING_LOGIN_ACTIVE_1)
        self.assertEqual(str(l_obj.UUID), TESTING_LOGIN_UUID_1)
        self.assertEqual(l_obj.LoginFullName, TESTING_LOGIN_FULL_NAME_1)
        self.assertEqual(l_obj.LoginPasswordCurrent, TESTING_LOGIN_PASSWORD_1)
        self.assertEqual(l_obj.LoginRole, TESTING_LOGIN_ROLE_1)

    def test_04_AllLogins(self):
        """ Read all login objects.
        """
        l_xml = self.m_xml.web_sect
        l_obj, l_count = webXml._read_all_logins(l_xml)
        # print(PrettyFormatAny.form(l_xml, 'B1-04-A - XML'))
        # print(PrettyFormatAny.form(l_obj, 'B1-04-B - All login'))
        # print(PrettyFormatAny.form(l_obj[0], 'B1-04-C - All login'))
        self.assertEqual(l_count, 2)
        self.assertEqual(len(l_obj), 2)

    def test_05_Web(self):
        """ Read all Web info.
        """
        self.m_pyhouse_obj.Computer.Web = webXml.read_web_xml(self.m_pyhouse_obj)
        l_obj = webXml.read_web_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'All Web'))
        self.assertEqual(l_obj.WebPort, int(TESTING_WEB_PORT))
        self.assertEqual(len(l_obj.Logins), 2)


class B2_Write(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_web_obj = webXml.read_web_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Web = self.m_web_obj
        self.m_web_xml = ET.Element("WebSection")

    def test_01_Ports(self):
        """ Write Web port.
        """
        # print(PrettyFormatAny.form(self.m_web_obj, 'B2-01-A - Web', 100))
        webXml._write_ports(self.m_web_obj, self.m_web_xml)
        # print(PrettyFormatAny.form(self.m_web_xml, 'B2-01-B - Web'))
        self.assertEqual(self.m_web_xml.find('Port').text, TESTING_WEB_PORT)
        self.assertEqual(self.m_web_xml.find('SecurePort').text, TESTING_WEB_SECURE_PORT)
        self.assertEqual(self.m_web_xml.find('SocketPort').text, TESTING_WEB_SOCKET_PORT)

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
        # print(PrettyFormatAny.form(l_obj, 'B2-03-A - Web'))
        l_xml = webXml._write_all_logins(l_obj)
        # print(PrettyFormatAny.form(l_xml, 'B2-03-B - Web'))
        self.assertEqual(l_xml.find('Login/FullName').text, TESTING_LOGIN_FULL_NAME_0)
        #
        l_xml = webXml._write_all_logins({})
        # print(PrettyFormatAny.form(l_xml, 'B2-03-C - Web'))

    def test_04_Web(self):
        """ Write All logins.
        """
        l_xml = webXml.write_web_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'B2-04-A - Web'))
        self.assertEqual(l_xml.find('Port').text, TESTING_WEB_PORT)
        self.assertEqual(l_xml.find('LoginSection/Login/FullName').text, TESTING_LOGIN_FULL_NAME_0)

# ## END DBK
