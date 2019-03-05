"""
@name:      PyHouse/src/Modules/Computer/Bridges/test/test_bridges_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@note:      Created on Dec 23, 2017
@license:   MIT License
@summary:

Passed all 12 tests - DBK - 2018-02-12

"""

__updated__ = '2019-02-24'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities import json_tools
from Modules.Core.Utilities import convert
from Modules.Computer.test.xml_computer import TESTING_COMPUTER_DIVISION
from Modules.Computer.Bridges.bridges_xml import Xml as bridgesXML
from Modules.Computer.Bridges.test.xml_bridges import \
    TESTING_BRIDGES_SECTION, \
    TESTING_BRIDGE, \
    XML_BRIDGES, \
    TESTING_BRIDGE_NAME_0, \
    TESTING_BRIDGE_KEY_0, \
    TESTING_BRIDGE_ACTIVE_0, \
    TESTING_BRIDGE_UUID_0, \
    TESTING_BRIDGE_IPV4ADDRESS_0, \
    TESTING_BRIDGE_PORT_0, \
    TESTING_BRIDGE_USERNAME_0, \
    TESTING_BRIDGE_PASSWORD_0, \
    TESTING_BRIDGE_COMMENT_0, \
    TESTING_BRIDGE_CONNECTION_0, \
    TESTING_BRIDGE_TYPE_0, \
    TESTING_BRIDGE_NAME_1, \
    TESTING_BRIDGE_KEY_1, \
    TESTING_BRIDGE_ACTIVE_1, \
    TESTING_BRIDGE_UUID_1, \
    TESTING_BRIDGE_IPV4ADDRESS_1, \
    TESTING_BRIDGE_PORT_1, \
    TESTING_BRIDGE_USERNAME_1, \
    TESTING_BRIDGE_PASSWORD_1, \
    TESTING_BRIDGE_COMMENT_1, \
    TESTING_BRIDGE_CONNECTION_1, \
    TESTING_BRIDGE_TYPE_1, \
    TESTING_BRIDGE_HUE_ACCESS_KEY_1
# from Modules.Core.Utilities.debug_tools import FormatBytes
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)

    def jsonPair(self, p_json, p_key):
        """ Extract key, value from json
        """
        l_json = json_tools.decode_json_unicode(p_json)
        try:
            l_val = l_json[p_key]
        except (KeyError, ValueError) as e_err:
            l_val = 'ERRor on JsonPair for key "{}"  {} {}'.format(p_key, e_err, l_json)
            print(l_val)
        return l_val


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_bridges')


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Tags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, TESTING_COMPUTER_DIVISION)
        self.assertEqual(self.m_xml.bridges_sect.tag, TESTING_BRIDGES_SECTION)
        self.assertEqual(self.m_xml.bridge.tag, TESTING_BRIDGE)


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))

    def test_01_Raw(self):
        l_raw = XML_BRIDGES
        # print('A2-01-A - Raw', l_raw)
        self.assertEqual(l_raw[:16], '<BridgesSection>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_BRIDGES)
        print('A2-02-A - Parsed', PrettyFormatAny.form(l_xml, 'A2-02-A Parsed'))
        self.assertEqual(l_xml.tag, TESTING_BRIDGES_SECTION)


class B1_Read(SetupMixin, unittest.TestCase):
    """ Test Reading of XML
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Bridge0(self):
        l_xml = self.m_xml.bridges_sect[0]
        l_obj = bridgesXML._read_one_bridge(l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-01-A - Bridge 0'))
        self.assertEqual(l_obj.Name, TESTING_BRIDGE_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_BRIDGE_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_BRIDGE_ACTIVE_0)
        self.assertEqual(l_obj.UUID, TESTING_BRIDGE_UUID_0)
        self.assertEqual(l_obj.IPv4Address, convert.str_to_long(TESTING_BRIDGE_IPV4ADDRESS_0))
        self.assertEqual(l_obj.TcpPort, int(TESTING_BRIDGE_PORT_0))
        self.assertEqual(l_obj.UserName, TESTING_BRIDGE_USERNAME_0)
        self.assertEqual(l_obj.Password, TESTING_BRIDGE_PASSWORD_0)
        self.assertEqual(l_obj.Comment, TESTING_BRIDGE_COMMENT_0)
        self.assertEqual(l_obj.Connection, TESTING_BRIDGE_CONNECTION_0)
        self.assertEqual(l_obj.Type, TESTING_BRIDGE_TYPE_0)

    def test_02_Bridge1(self):
        """ A Philips Hue Bridge
        """
        l_xml = self.m_xml.bridges_sect[1]
        l_obj = bridgesXML._read_one_bridge(l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-02-A - Bridge 1'))
        self.assertEqual(l_obj.Name, TESTING_BRIDGE_NAME_1)
        self.assertEqual(str(l_obj.Key), TESTING_BRIDGE_KEY_1)
        self.assertEqual(str(l_obj.Active), TESTING_BRIDGE_ACTIVE_1)
        self.assertEqual(l_obj.UUID, TESTING_BRIDGE_UUID_1)
        self.assertEqual(l_obj.IPv4Address, convert.str_to_long(TESTING_BRIDGE_IPV4ADDRESS_1))
        self.assertEqual(l_obj.TcpPort, int(TESTING_BRIDGE_PORT_1))
        self.assertEqual(l_obj.UserName, TESTING_BRIDGE_USERNAME_1)
        self.assertEqual(l_obj.Password, TESTING_BRIDGE_PASSWORD_1)
        self.assertEqual(l_obj.Comment, TESTING_BRIDGE_COMMENT_1)
        self.assertEqual(l_obj.Connection, TESTING_BRIDGE_CONNECTION_1)
        self.assertEqual(l_obj.Type, TESTING_BRIDGE_TYPE_1)
        self.assertEqual(l_obj.ApiKey, TESTING_BRIDGE_HUE_ACCESS_KEY_1)

    def test_03_Bridges(self):
        """Here we should get a dict of bridges
        """
        l_obj = bridgesXML.read_bridges_xml(self.m_pyhouse_obj, self)
        # print(PrettyFormatAny.form(l_obj, 'B1-03-A - All Bridges'))
        # print(PrettyFormatAny.form(l_obj[0], 'B1-03-B - All Bridges'))
        # print(PrettyFormatAny.form(l_obj[1], 'B1-03-C - All Bridges'))
        self.assertEqual(l_obj[0].Name, TESTING_BRIDGE_NAME_0)
        self.assertEqual(str(l_obj[0].Key), TESTING_BRIDGE_KEY_0)
        self.assertEqual(str(l_obj[0].Active), TESTING_BRIDGE_ACTIVE_0)
        self.assertEqual(l_obj[1].Name, TESTING_BRIDGE_NAME_1)
        self.assertEqual(str(l_obj[1].Key), TESTING_BRIDGE_KEY_1)
        self.assertEqual(str(l_obj[1].Active), TESTING_BRIDGE_ACTIVE_1)

    def test_04_Valid(self):
        """
        """
        l_xml = self.m_xml.bridges_sect[1]
        l_type = bridgesXML()._read_type(l_xml)
        # print(PrettyFormatAny.form(l_type, 'B1-04-A - Type'))
        self.assertEqual(l_type, TESTING_BRIDGE_TYPE_1)

    def test_05_InValid(self):
        """
        """
        l_xml = self.m_xml.bridges_sect[1]
        l_xml.find('Type').text = 'Garbage'
        l_type = bridgesXML()._read_type(l_xml)
        # print(PrettyFormatAny.form(l_type, 'B1-05-A - Type'))
        self.assertEqual(l_type, 'Null')


class C1_Write(SetupMixin, unittest.TestCase):
    """ Test Reading of XML
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Bridge0(self):
        """Write one bridge
        """
        l_xml_r = self.m_xml.bridges_sect[0]
        l_obj = bridgesXML._read_one_bridge(l_xml_r)
        # print(PrettyFormatAny.form(l_obj, 'C1-01-A - Bridge 0'))
        l_xml = bridgesXML._write_one_bridge(l_obj)
        # print(PrettyFormatAny.form(l_xml, 'C1-01-B - Bridge 0'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_BRIDGE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_BRIDGE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_BRIDGE_ACTIVE_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_BRIDGE_COMMENT_0)
        self.assertEqual(l_xml.find('Connection').text, TESTING_BRIDGE_CONNECTION_0)
        self.assertEqual(l_xml.find('Type').text, TESTING_BRIDGE_TYPE_0)
        self.assertEqual(l_xml.find('IPv4Address').text, TESTING_BRIDGE_IPV4ADDRESS_0)
        self.assertEqual(l_xml.find('Port').text, TESTING_BRIDGE_PORT_0)
        self.assertEqual(l_xml.find('UserName').text, TESTING_BRIDGE_USERNAME_0)
        self.assertEqual(l_xml.find('Password').text, TESTING_BRIDGE_PASSWORD_0)

    def test_02_Bridge1(self):
        """Write one bridge (Hue Bridge) XML
        """
        l_xml_r = self.m_xml.bridges_sect[1]
        l_obj = bridgesXML._read_one_bridge(l_xml_r)
        # print(PrettyFormatAny.form(l_xml_r, 'C1-02-A - Bridge 1'))
        l_xml = bridgesXML._write_one_bridge(l_obj)
        # print(PrettyFormatAny.form(l_xml, 'C1-02-B - Bridge 0'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_BRIDGE_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_BRIDGE_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_BRIDGE_ACTIVE_1)
        self.assertEqual(l_xml.find('Comment').text, TESTING_BRIDGE_COMMENT_1)
        self.assertEqual(l_xml.find('Connection').text, TESTING_BRIDGE_CONNECTION_1)
        self.assertEqual(l_xml.find('Type').text, TESTING_BRIDGE_TYPE_1)
        self.assertEqual(l_xml.find('IPv4Address').text, TESTING_BRIDGE_IPV4ADDRESS_1)
        self.assertEqual(l_xml.find('Port').text, TESTING_BRIDGE_PORT_1)
        self.assertEqual(l_xml.find('UserName').text, TESTING_BRIDGE_USERNAME_1)
        self.assertEqual(l_xml.find('Password').text, TESTING_BRIDGE_PASSWORD_1)
        self.assertEqual(l_xml.find('Password').text, TESTING_BRIDGE_PASSWORD_1)
        self.assertEqual(l_xml.find('ApiKey').text, TESTING_BRIDGE_HUE_ACCESS_KEY_1)

    def test_03_Bridges(self):
        """Write all bridges
        """
        l_obj = bridgesXML.read_bridges_xml(self.m_pyhouse_obj, self)
        self.m_pyhouse_obj.Computer.Bridges = l_obj
        # print(PrettyFormatAny.form(l_obj, 'C1-03-A - Bridges'))
        l_sect_xml = bridgesXML.write_bridges_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_sect_xml, 'C1-03-B - Bridges'))
        l_xml = l_sect_xml[0]
        self.assertEqual(l_xml.attrib['Name'], TESTING_BRIDGE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_BRIDGE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_BRIDGE_ACTIVE_0)
        l_xml = l_sect_xml[1]
        self.assertEqual(l_xml.attrib['Name'], TESTING_BRIDGE_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_BRIDGE_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_BRIDGE_ACTIVE_1)

# ## END DBK
