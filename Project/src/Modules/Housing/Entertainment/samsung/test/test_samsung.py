"""
@name:      PyHouse/src/Modules/Housing/Entertainment/test/test_samsung.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 14, 2016
@summary:

Passed all 15 tests - DBK - 2018-10-17

"""

__updated__ = '2019-06-30'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities import convert
from Modules.Housing.Entertainment.entertainment_data import \
        EntertainmentInformation, \
        EntertainmentPluginInformation
from Modules.Housing.Entertainment.samsung.samsung import XML as samsungXml, SECTION
from Modules.Housing.Entertainment.test.xml_entertainment import \
        TESTING_ENTERTAINMENT_SECTION
from Modules.Housing.test.xml_housing import \
        TESTING_HOUSE_NAME, \
        TESTING_HOUSE_ACTIVE, \
        TESTING_HOUSE_KEY, \
        TESTING_HOUSE_UUID, \
        TESTING_HOUSE_DIVISION
from Modules.Housing.Entertainment.samsung.test.xml_samsung import \
        TESTING_SAMSUNG_DEVICE_NAME_0, \
        TESTING_SAMSUNG_DEVICE_KEY_0, \
        TESTING_SAMSUNG_DEVICE_ACTIVE_0, \
        TESTING_SAMSUNG_DEVICE_UUID_0, \
        TESTING_SAMSUNG_DEVICE_IPV4_0, \
        TESTING_SAMSUNG_DEVICE_PORT_0, \
        TESTING_SAMSUNG_SECTION, \
        XML_SAMSUNG_SECTION, \
        TESTING_SAMSUNG_DEVICE_COMMENT_0, TESTING_SAMSUNG_DEVICE_COMMAND_SET_0
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_samsung')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        l_xml = self.m_xml.entertainment_sect
        # print(PrettyFormatAny.form(l_xml, 'A1-01-A - Entertainment XML'))
        self.assertIsNotNone(l_xml.find(TESTING_SAMSUNG_SECTION))

    def test_02_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-02-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)
        self.assertEqual(self.m_xml.entertainment_sect.tag, TESTING_ENTERTAINMENT_SECTION)
        self.assertEqual(self.m_xml.samsung_sect.tag, TESTING_SAMSUNG_SECTION)

    def test_03_PyHouse(self):
        l_obj = self.m_pyhouse_obj
        # print(PrettyFormatAny.form(l_obj, 'A1-03-A - PyHouse'))
        # print(PrettyFormatAny.form(l_obj.House, 'A1-03-B - House'))
        # print(PrettyFormatAny.form(l_obj.House.Entertainment, 'A1-03-C - Entertainment'))
        # print(PrettyFormatAny.form(l_obj.House.Entertainment, 'A1-03-D - Samsung'))
        # self.assertIs(self.m_pyhouse_obj.House, HouseInformation())


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_SAMSUNG_SECTION
        # print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[1:len(TESTING_SAMSUNG_SECTION) + 1], TESTING_SAMSUNG_SECTION)

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_SAMSUNG_SECTION)
        # print('A2-02-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'Parsed')))
        self.assertEqual(l_xml.tag, TESTING_SAMSUNG_SECTION)


class A3_XML(SetupMixin, unittest.TestCase):
    """ Now we test that the xml_xxxxx have set up the XML_LONG tree properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_HouseDivXml(self):
        """ Test
        """
        l_xml = self.m_xml.house_div
        # print(PrettyFormatAny.form(l_xml, 'A3-01-A - House'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_HOUSE_NAME)
        self.assertEqual(l_xml.attrib['Active'], TESTING_HOUSE_ACTIVE)
        self.assertEqual(l_xml.attrib['Key'], TESTING_HOUSE_KEY)
        self.assertEqual(l_xml.find('UUID').text, TESTING_HOUSE_UUID)

    def test_02_EntertainmentXml(self):
        """ Test
        """
        l_xml = self.m_xml.entertainment_sect
        # print(PrettyFormatAny.form(l_xml, 'A3-02-A - Entertainment'))
        self.assertEqual(len(l_xml), 5)

    def test_03_SamsungXml(self):
        """ Test
        """
        l_xml = self.m_xml.samsung_sect
        # print(PrettyFormatAny.form(l_xml, 'A3-03-A - Samsung'))
        self.assertEqual(len(l_xml), 1)
        self.assertEqual(l_xml[0].attrib['Name'], TESTING_SAMSUNG_DEVICE_NAME_0)

    def test_04_Device0(self):
        """ Be sure that the XML contains everything in RoomInformation().
        """
        l_xml = self.m_xml.samsung_sect.find('Device')
        # print(PrettyFormatAny.form(l_xml, 'A3-04-A Device'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_SAMSUNG_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_SAMSUNG_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_SAMSUNG_DEVICE_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_SAMSUNG_DEVICE_UUID_0)
        self.assertEqual(l_xml.find('IPv4').text, TESTING_SAMSUNG_DEVICE_IPV4_0)
        self.assertEqual(l_xml.find('Port').text, TESTING_SAMSUNG_DEVICE_PORT_0)


class C1_Read(SetupMixin, unittest.TestCase):
    """ Test that we read in the XML config properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.Entertainment = EntertainmentInformation()
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginInformation()
        self.m_xml_pioneer = self.m_xml.pioneer_sect.find('Device')

    def test_01_Device(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj = samsungXml._read_device(self.m_xml.samsung_sect.find('Device'))
        print(PrettyFormatAny.form(l_obj, 'C1-01-A - Device'))
        self.assertEqual(l_obj.Name, TESTING_SAMSUNG_DEVICE_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_SAMSUNG_DEVICE_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_SAMSUNG_DEVICE_ACTIVE_0)
        self.assertEqual(l_obj.UUID, TESTING_SAMSUNG_DEVICE_UUID_0)
        #
        self.assertEqual(convert.long_to_str(l_obj.IPv4), TESTING_SAMSUNG_DEVICE_IPV4_0)
        self.assertEqual(str(l_obj.Port), TESTING_SAMSUNG_DEVICE_PORT_0)
        self.assertEqual(str(l_obj.CommandSet), TESTING_SAMSUNG_DEVICE_COMMAND_SET_0)

    def test_02_AllDevices(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj = samsungXml.read_samsung_section_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_obj, 'C1-02-A - All Devices'))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'C1-02-B - All Devices'))


class D1_Write(SetupMixin, unittest.TestCase):
    """ Test that we read in the XML config properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.Entertainment = EntertainmentInformation()
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginInformation()
        self.m_section = samsungXml.read_samsung_section_xml(self.m_pyhouse_obj)
        # self.m_pyhouse_obj.House.Entertainment.Pioneer = self.m_section

    def test_01_Setup(self):
        """ Read the xml and fill in the first room's dict
        """
        pass
        # print(PrettyFormatAny.form(self.m_section, 'D1-01-A - Section'))
        # print(PrettyFormatAny.form(self.m_section.Devices[0], 'D1-01-B - One Device'))

    def test_02_OneDevice(self):
        """ Read the xml and fill in the first room's dict
        """
        l_xml = samsungXml._write_device(self.m_section.Devices[0])
        # print(PrettyFormatAny.form(l_xml, 'D1-02-A - One Device'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_SAMSUNG_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_SAMSUNG_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_SAMSUNG_DEVICE_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_SAMSUNG_DEVICE_UUID_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_SAMSUNG_DEVICE_COMMENT_0)

    def test_03_AllDevices(self):
        """
        """
        l_xml = samsungXml.write_samsung_section_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'D1-03-A - XML'))
        self.assertEqual(l_xml.find('Device').attrib['Name'], TESTING_SAMSUNG_DEVICE_NAME_0)
        self.assertEqual(l_xml.find('Device').attrib['Key'], TESTING_SAMSUNG_DEVICE_KEY_0)
        self.assertEqual(l_xml.find('Device').attrib['Active'], TESTING_SAMSUNG_DEVICE_ACTIVE_0)

# ## END DBK
