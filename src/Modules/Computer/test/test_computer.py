"""
@name:      PyHouse/src/Modules/Computer/test/test_computer.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 25, 2014
@Summary:

Passed all 10 tests - DBK - 2017-01-14

"""
__updated__ = "2017-12-21"

# Import system type stuff
import platform
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Computer.computer import API as computerAPI, Xml as computerXML, COMPUTER_DIVISION
from Modules.Computer.test.xml_computer import \
    TESTING_COMPUTER_NAME_0, \
    TESTING_COMPUTER_DIVISION, \
    TESTING_COMPUTER_KEY_0, \
    TESTING_COMPUTER_ACTIVE_0
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = computerAPI(self.m_pyhouse_obj)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_computer')


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Build'))
        self.assertEqual(self.m_pyhouse_obj.House.Rooms, {})

    def test_02_Tags(self):
        """ Be sure that the XML contains the right stuff.
        Test some scattered things so we don't end up with hundreds of asserts.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-02-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, TESTING_COMPUTER_DIVISION)


class A2_XML(SetupMixin, unittest.TestCase):
    """ Be sure that the XXML was created
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        Test some scattered things so we don't end up with hundreds of asserts.
        """
        # print(PrettyFormatAny.form(self.m_xml, A2-01-A - 'Xml'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, TESTING_COMPUTER_DIVISION)

    def test_02_Computer(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'A2-02-A - PyHouse'))
        self.assertEqual(self.m_xml.computer_div.tag, TESTING_COMPUTER_DIVISION)


class C1_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Create(self):
        """
        """
        l_xml = computerXML.create_computer_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'C1-01-A - Computer Xml'))
        self.assertEqual(l_xml.Name, platform.node())
        self.assertEqual(l_xml.Key, 0)
        # self.assertEqual(l_xml.Active, True)

    def test_02_Xml(self):
        """ Read the config - it is minimal.
        """
        l_obj = computerXML.read_computer_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'C1-02-A - Computer Xml'))
        self.assertEqual(l_obj.Name, TESTING_COMPUTER_NAME_0)


class C2_Write(SetupMixin, unittest.TestCase):

    @staticmethod
    def write_computer_xml(p_pyhouse_obj):
        l_xml = XmlConfigTools.write_base_UUID_object_xml(COMPUTER_DIVISION, p_pyhouse_obj.Computer)
        return l_xml

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        _l_obj = computerXML.read_computer_xml(self.m_pyhouse_obj)
        l_xml = computerXML.write_computer_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'C2-01-A - Computer Xml'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_COMPUTER_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_COMPUTER_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_COMPUTER_ACTIVE_0)

# # ## END DBK
