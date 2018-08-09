"""
@name:      PyHouse/src/Modules/entertain/test/test_pandora.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 22, 2014
@summary:   Test

Passed all 2 tests - DBK - 2016-11-22

"""
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.Utilities import convert

__updated__ = '2018-08-05'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from twisted.test import proto_helpers

# Import PyMh files
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Housing.Entertainment.pandora.pandora import \
        XML as pandoraXml
from Modules.Housing.Entertainment.pandora.test.xml_pandora import \
        XML_PANDORA_SECTION, \
        TESTING_PANDORA_DEVICE, \
        TESTING_PANDORA_SECTION, \
        L_PANDORA_SECTION_START, \
        TESTING_PANDORA_DEVICE_NAME_0, \
        TESTING_PANDORA_DEVICE_KEY_0, \
        TESTING_PANDORA_DEVICE_ACTIVE_0, TESTING_PANDORA_CONNECTION_DEVICE_0_0
from Modules.Housing.test.xml_housing import \
        TESTING_HOUSE_DIVISION, \
        TESTING_HOUSE_NAME, \
        TESTING_HOUSE_ACTIVE, \
        TESTING_HOUSE_KEY, \
        TESTING_HOUSE_UUID
from Modules.Housing.Entertainment.test.xml_entertainment import \
        TESTING_ENTERTAINMENT_SECTION


class SetupMixin:

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)

        # self.m_factory = pioFactory(self.m_pyhouse_obj)
        # self.m_transport = proto_helpers.StringTransport()
        # self.m_proto = self.m_factory.buildProtocol(('127.0.0.1', 0))
        # self.m_proto.makeConnection(self.m_transport)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_pandora')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly.
        """
        l_xml = self.m_xml.entertainment_sect
        # print(PrettyFormatAny.form(l_xml, 'A1-01-A - Entertainment XML'))
        self.assertIsNotNone(l_xml.find(TESTING_PANDORA_SECTION))

    def test_02_XmlTags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-02-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)
        self.assertEqual(self.m_xml.entertainment_sect.tag, TESTING_ENTERTAINMENT_SECTION)
        self.assertEqual(self.m_xml.pandora_sect.tag, TESTING_PANDORA_SECTION)


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_PANDORA_SECTION
        print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[:16], L_PANDORA_SECTION_START)

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_PANDORA_SECTION)
        print('A2-02-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'A2-02-A - Parsed')))
        self.assertEqual(l_xml.tag, TESTING_PANDORA_SECTION)


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
        self.assertGreater(len(l_xml), 2)

    def test_03_PandoraXml(self):
        """ Test
        """
        l_xml = self.m_xml.pandora_sect
        # print(PrettyFormatAny.form(l_xml, 'A3-03-A - Pioneer'))
        self.assertEqual(len(l_xml), 2)
        self.assertEqual(l_xml[0].attrib['Name'], TESTING_PANDORA_DEVICE_NAME_0)

    def test_04_Device0(self):
        """ Be sure that the XML contains everything in RoomData().
        """
        l_xml = self.m_xml.pandora_sect.find('Device')
        # print(PrettyFormatAny.form(l_xml, 'A3-04-A Device'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_PANDORA_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_PANDORA_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_PANDORA_DEVICE_ACTIVE_0)
        # self.assertEqual(l_xml.find('UUID').text, TESTING_PIONEER_DEVICE_UUID_0)
        # self.assertEqual(l_xml.find('IPv4').text, TESTING_PIONEER_DEVICE_IPV4_0)
        # self.assertEqual(l_xml.find('Port').text, TESTING_PIONEER_DEVICE_PORT_0)


class C1_Read(SetupMixin, unittest.TestCase):
    """ Test that we read in the XML config properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_OneDevice(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj = pandoraXml._read_one_entry(self.m_xml.pandora_sect.find('Device'))
        print(PrettyFormatAny.form(l_obj, 'B1-1-A - One Device'))
        self.assertEqual(l_obj.Name, TESTING_PANDORA_DEVICE_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_PANDORA_DEVICE_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_PANDORA_DEVICE_ACTIVE_0)
        # .
        self.assertEqual(convert.long_to_str(l_obj.IPv4), TESTING_PANDORA_CONNECTION_DEVICE_0_0)

    def test_2_AllDevices(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj = pandoraXml._read_one_entry(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_obj, 'B1-2-A - All Devices'))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'B1-2-AB - All Devices'))

# ## END DBK
