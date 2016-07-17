"""
@name:      /home/briank/PyHouse/src/Modules/Housing/Entertainment/test/test_samsung.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 14, 2016
@summary:

Passed all 7 tests - DBK - 2016-07-15

"""

__updated__ = '2016-07-15'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Housing.Entertainment.samsung import Xml as samsungXml
from Modules.Housing.test.xml_housing import \
    TESTING_HOUSE_NAME, \
    TESTING_HOUSE_ACTIVE, \
    TESTING_HOUSE_KEY, \
    TESTING_HOUSE_UUID
from Modules.Housing.Entertainment.test.xml_entertainment import \
    TESTING_SAMSUNG_DEVICE_NAME_0, \
    TESTING_SAMSUNG_DEVICE_KEY_0, \
    TESTING_SAMSUNG_DEVICE_ACTIVE_0, \
    TESTING_SAMSUNG_DEVICE_UUID_0, \
    TESTING_SAMSUNG_DEVICE_IPV4_0, \
    TESTING_SAMSUNG_DEVICE_PORT_0
from Modules.Utilities import convert
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)

class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Tags'))
        self.assertEqual(self.m_pyhouse_obj.House.Rooms, None)

    def test_2_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Tags'))
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.entertainment_sect.tag, 'EntertainmentSection')
        self.assertEqual(self.m_xml.samsung_sect.tag, 'SamsungSection')
        self.assertEqual(self.m_xml.room.tag, 'Room')


class A2_XML(SetupMixin, unittest.TestCase):
    """ Now we test that the xml_xxxxx have set up the XML_LONG tree properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_HouseDivXml(self):
        """ Test
        """
        l_xml = self.m_xml.house_div
        # print(PrettyFormatAny.form(l_xml, 'A2-1-A - House'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_HOUSE_NAME)
        self.assertEqual(l_xml.attrib['Active'], TESTING_HOUSE_ACTIVE)
        self.assertEqual(l_xml.attrib['Key'], TESTING_HOUSE_KEY)
        self.assertEqual(l_xml.find('UUID').text, TESTING_HOUSE_UUID)

    def test_2_EntertainmentXml(self):
        """ Test
        """
        l_xml = self.m_xml.entertainment_sect
        print(PrettyFormatAny.form(l_xml, 'A2-2-A - Entertainment'))
        self.assertEqual(len(l_xml), 1)

    def test_3_SamsungXml(self):
        """ Test
        """
        l_xml = self.m_xml.samsung_sect
        # print(PrettyFormatAny.form(l_xml, 'A2-3-A - Samsung'))
        self.assertEqual(len(l_xml), 1)
        self.assertEqual(l_xml[0].attrib['Name'], TESTING_SAMSUNG_DEVICE_NAME_0)

    def test_4_Device0(self):
        """ Be sure that the XML contains everything in RoomData().
        """
        l_xml = self.m_xml.samsung_sect.find('Device')
        # print(PrettyFormatAny.form(l_xml, 'A2-2-A Device'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_SAMSUNG_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_SAMSUNG_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_SAMSUNG_DEVICE_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_SAMSUNG_DEVICE_UUID_0)
        self.assertEqual(l_xml.find('IPv4').text, TESTING_SAMSUNG_DEVICE_IPV4_0)
        self.assertEqual(l_xml.find('Port').text, TESTING_SAMSUNG_DEVICE_PORT_0)


class B1_Read(SetupMixin, unittest.TestCase):
    """ Test that we read in the XML config properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_OneDevice(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj = samsungXml._read_one_device(self.m_xml.samsung_sect.find('Device'))
        print(PrettyFormatAny.form(l_obj, 'B1-1-A - One Device'))
        self.assertEqual(l_obj.Name, TESTING_SAMSUNG_DEVICE_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_SAMSUNG_DEVICE_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_SAMSUNG_DEVICE_ACTIVE_0)
        self.assertEqual(l_obj.UUID, TESTING_SAMSUNG_DEVICE_UUID_0)
        # .
        self.assertEqual(convert.long_to_str(l_obj.IPv4), TESTING_SAMSUNG_DEVICE_IPV4_0)
        self.assertEqual(str(l_obj.Port), TESTING_SAMSUNG_DEVICE_PORT_0)

    def test_2_AllDevices(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj = samsungXml.read_samsung_section_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_obj, 'B1-2-A - All Devices'))


class C1_Write(SetupMixin, unittest.TestCase):
    """ Test that we read in the XML config properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_OneDevice(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj = samsungXml._read_one_device(self.m_xml.samsung_sect.find('Device'))
        print(PrettyFormatAny.form(l_obj, 'C1-1-A - One Device'))
        self.assertEqual(l_obj.Name, TESTING_SAMSUNG_DEVICE_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_SAMSUNG_DEVICE_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_SAMSUNG_DEVICE_ACTIVE_0)
        self.assertEqual(l_obj.UUID, TESTING_SAMSUNG_DEVICE_UUID_0)
        # .
        self.assertEqual(convert.long_to_str(l_obj.IPv4), TESTING_SAMSUNG_DEVICE_IPV4_0)
        self.assertEqual(str(l_obj.Port), TESTING_SAMSUNG_DEVICE_PORT_0)

    def test_2_AllDevices(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj = samsungXml._read_one_device(self.m_xml.samsung_sect.find('Device'))
        print(PrettyFormatAny.form(l_obj, 'C2-2-A - All Devices'))


# ## END DBK
