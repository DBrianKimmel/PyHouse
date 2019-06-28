"""
@name:      PyHouse/src/Modules.Core.Utilities.test/test_node_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun  9, 2019
@Summary:

Passed all 5 tests - DBK - 2019-06-09

"""

__updated__ = '2019-06-09'

# Import system type stuff
from twisted.trial import unittest
from xml.etree import ElementTree as ET

# Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Housing.test.xml_housing import TESTING_HOUSE_DIVISION
from Modules.Computer.test.xml_computer import TESTING_COMPUTER_DIVISION, XML_COMPUTER_DIVISION


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_device_tools')


class A1_Setup(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Find(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)
        self.assertEqual(self.m_xml.computer_div.tag, TESTING_COMPUTER_DIVISION)

    def test_02_XML(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml.light, 'A1-02-A - Base'))
        pass


class A2_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))

    def test_01_Raw(self):
        l_raw = XML_COMPUTER_DIVISION
        # print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[1:len(TESTING_COMPUTER_DIVISION) + 1], TESTING_COMPUTER_DIVISION)

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_COMPUTER_DIVISION)
        # print('A2-02-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'Parsed')))
        self.assertEqual(l_xml.tag, TESTING_COMPUTER_DIVISION)


class B1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))

    def test_01_Raw(self):
        l_raw = XML_COMPUTER_DIVISION
        # print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[1:len(TESTING_COMPUTER_DIVISION) + 1], TESTING_COMPUTER_DIVISION)

# ## END DBK
