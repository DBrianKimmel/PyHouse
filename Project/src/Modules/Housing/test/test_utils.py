"""
@name:      PyHouse/src/Modules/Housing/test/test_utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 23, 2016
@summary:   Test

passed all 6 tests - DBK - 2018-02-13

"""
from Modules.Housing.test.xml_housing import TESTING_HOUSE_DIVISION

__updated__ = '2019-06-09'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import DeviceData
from Modules.Housing import utils
from Modules.Housing.test.xml_rooms import \
    TESTING_ROOM_NAME_0, \
    TESTING_ROOM_KEY_0, \
    TESTING_ROOM_ACTIVE_0
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_utils')


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Tags(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_onkyo_xml = self.m_xml.entertainment_sect.find('OnkyoSection')
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)
        self.assertEqual(l_onkyo_xml.tag, 'OnkyoSection')


class A2_XML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by Onkyo.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Rooms(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_xml = self.m_xml.room_sect
        # print(PrettyFormatAny.form(l_xml, 'A2-01-A - XML'))
        self.assertEqual(len(l_xml), 4)

    def test_02_Room0(self):
        """Ensure that the lighting objects are correct in the XML
        """
        l_xml = self.m_xml.room
        # print(PrettyFormatAny.form(l_xml, 'A2-02-A - PyHouse'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ROOM_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ROOM_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ROOM_ACTIVE_0)


class B1_Rooms(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def tearDown(self):
        pass

    def test_01_Read(self):
        l_xml = ET.Element('TestElement')
        l_obj = DeviceData()
        utils.read_room_reference_xml(l_obj, l_xml)
        print(PrettyFormatAny.form(l_obj, 'B1-01-A - Data'))

    def test_02_Write(self):
        l_xml = ET.Element('TestElement')
        l_obj = DeviceData()
        utils.read_room_reference_xml(l_obj, l_xml)
        print(PrettyFormatAny.form(l_obj, 'B1-02-A - Data'))

# ## END DBK
