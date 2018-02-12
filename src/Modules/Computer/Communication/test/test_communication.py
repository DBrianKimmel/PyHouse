"""
@name:       PyHouse/src/Modules/Computer/Communication/test/test_communication.py
@author:     D. Brian Kimmel
@contact:    d.briankimmel@gmail.com
@copyright:  2016-2017 by D. Brian Kimmel
@date:       Created on May 30, 2016
@licencse:   MIT License
@summary:

Passed all 5 tests - DBK - 2017-01-19

"""

__updated__ = '2018-02-12'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Computer.test.xml_computer import \
    TESTING_COMPUTER_DIVISION
from Modules.Computer.Communication.test.xml_communications import \
    XML_COMMUNICATION, \
    TESTING_COMMUNICATION_SECTION, \
    TESTING_EMAIL_SECTION
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny


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
        print('Id: test_communications')


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_pyhouse_obj.Computer.Communication, {})

    def test_02_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, TESTING_COMPUTER_DIVISION)
        self.assertEqual(self.m_xml.email_sect.tag, TESTING_EMAIL_SECTION)


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_COMMUNICATION
        # print(l_raw)
        self.assertEqual(l_raw[:22], '<CommunicationSection>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_COMMUNICATION)
        # print(l_xml)
        self.assertEqual(l_xml.tag, TESTING_COMMUNICATION_SECTION)

# ## END DBK
