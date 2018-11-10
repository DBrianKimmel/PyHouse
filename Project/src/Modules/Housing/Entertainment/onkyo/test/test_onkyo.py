"""
@name:      PyHouse/src/Modules/Housing/Entertainment/test/test_onkyo.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 22, 2014
@summary:   Test

Run 'PyHouse/src/test/test_xml_data.py' if XML is corrupted.

Passed all 8 tests - DBK - 2018-11-03

"""

__updated__ = '2018-11-03'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from Modules.Housing.Entertainment.onkyo.onkyo import SECTION, API as onkyoAPI
from Modules.Core.Utilities import convert
from Modules.Housing.Entertainment.entertainment_data import EntertainmentData, EntertainmentPluginData
from Modules.Housing.Entertainment.test.xml_entertainment import \
        TESTING_ENTERTAINMENT_SECTION
from Modules.Housing.Entertainment.onkyo.test.xml_onkyo import \
        TESTING_ONKYO_DEVICE_UUID_0, \
        TESTING_ONKYO_DEVICE_KEY_0, \
        TESTING_ONKYO_DEVICE_NAME_0, \
        TESTING_ONKYO_DEVICE_ACTIVE_0, \
        TESTING_ONKYO_DEVICE_IPV4_0, \
        TESTING_ONKYO_DEVICE_PORT_0, \
        TESTING_ONKYO_DEVICE_COMMENT_0, \
        TESTING_ONKYO_DEVICE_TYPE_0, \
        TESTING_ONKYO_SECTION, \
        TESTING_ONKYO_DEVICE_NAME_1, \
        TESTING_ONKYO_DEVICE_KEY_1, \
        TESTING_ONKYO_DEVICE_ACTIVE_1, \
        TESTING_ONKYO_DEVICE_UUID_1, \
        TESTING_ONKYO_DEVICE_VOLUME_0, \
        TESTING_ONKYO_DEVICE_ROOM_NAME_0, \
        TESTING_ONKYO_DEVICE_ROOM_UUID_0, \
        TESTING_ONKYO_DEVICE_VOLUME_1, \
        XML_ONKYO_SECTION, \
        TESTING_ONKYO_TYPE, \
        TESTING_ONKYO_ACTIVE
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_pyhouse_obj.House.Entertainment = EntertainmentData()
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_onkyo')


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Objects(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_onkyo_xml = self.m_xml.entertainment_sect.find(TESTING_ONKYO_SECTION)
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.entertainment_sect.tag, 'EntertainmentSection')
        self.assertEqual(l_onkyo_xml.tag, 'OnkyoSection')


class A2_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_ONKYO_SECTION
        # print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[1:len(TESTING_ONKYO_SECTION) + 1], TESTING_ONKYO_SECTION)

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_ONKYO_SECTION)
        # print('A2-02-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'Parsed')))
        self.assertEqual(l_xml.tag, TESTING_ONKYO_SECTION)


class A3_XML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by Onkyo.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Entertainment(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_xml = self.m_xml.house_div
        l_ret = l_xml.find('EntertainmentSection')
        # print(PrettyFormatAny.form(l_ret, 'A2-01-B - XML'))
        self.assertEqual(l_ret.tag, TESTING_ENTERTAINMENT_SECTION)

    def test_02_Onkyo(self):
        """Ensure that the lighting objects are correct in the XML
        """
        l_xml = self.m_xml.entertainment_sect.find('OnkyoSection')
        # print(PrettyFormatAny.form(l_xml, 'A2-02-A - PyHouse'))
        self.assertEqual(l_xml.tag, TESTING_ONKYO_SECTION)

    def test_03_Device0(self):
        """Ensure that the lighting objects are correct in the XML
        """
        l_xml = self.m_xml.onkyo_sect.findall('Device')[0]
        # print(PrettyFormatAny.form(l_xml, 'A2-03-A - PyHouse'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ONKYO_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ONKYO_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ONKYO_DEVICE_ACTIVE_0)

    def test_04_Device1(self):
        """Ensure that the lighting objects are correct in the XML
        """
        l_xml = self.m_xml.onkyo_sect.findall('Device')[1]
        # print(PrettyFormatAny.form(l_xml, 'A2-04-A - PyHouse'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ONKYO_DEVICE_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ONKYO_DEVICE_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ONKYO_DEVICE_ACTIVE_1)

# ## END DBK
