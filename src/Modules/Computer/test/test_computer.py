"""
@name:      PyHouse/src/Modules/Computer/test/test_computer.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 25, 2014
@Summary:

Passed all 7 tests - DBK - 2016-07-06

"""
__updated__ = "2016-07-06"

# Import system type stuff
import platform
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Computer.computer import API as computerAPI, Xml as computerXML

from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny
from Modules.Computer.test.xml_computer import TESTING_COMPUTER_NAME_0

DIVISION = 'ComputerDivision'
MQTT_SECTION = 'MqttSection'


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = computerAPI(self.m_pyhouse_obj)


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        Test some scattered things so we don't end up with hundreds of asserts.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Xml'))
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.computer_div.tag, DIVISION)
        self.assertEqual(self.m_xml.mqtt_sect.tag, MQTT_SECTION)

    def test_02_Computer(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'PyHouse'))
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')


class B1_XML(SetupMixin, unittest.TestCase):
    """ Be sure that the XXML was created
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        Test some scattered things so we don't end up with hundreds of asserts.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Xml'))
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.computer_div.tag, DIVISION)
        self.assertEqual(self.m_xml.mqtt_sect.tag, MQTT_SECTION)

    def test_02_Computer(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'PyHouse'))
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')


class C1_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Create(self):
        """
        """
        l_xml = computerXML.create_computer(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_xml, 'C1-01-A - Computer Xml'))
        self.assertEqual(l_xml.Name, platform.node())
        self.assertEqual(l_xml.Key, 0)
        self.assertEqual(l_xml.Active, True)

    def test_02_Xml(self):
        """ Read the config - it is minimal.
        """
        l_obj = computerXML.read_computer_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_obj, 'C1-02-A - Computer Xml'))
        self.assertEqual(l_obj.Name, TESTING_COMPUTER_NAME_0)


class C2_Write(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        _l_obj = computerXML.read_computer_xml(self.m_pyhouse_obj)
        l_xml = computerXML.write_computer_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_xml, 'C2-01-A - Computer Xml'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_COMPUTER_NAME_0)

# # ## END DBK
