"""
@name:      PyHouse/src/Modules/Housing/Entertainment/pioneer/test/test_pioneer.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 10, 2018
@summary:   Test

Passed all 16 tests - DBK - 2018-07-11

"""

__updated__ = '2018-07-15'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from twisted.test import proto_helpers

# Import PyMh files
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities import convert
from Modules.Housing.Entertainment.pioneer.pioneer import \
        XML as pioneerXml, \
        PioneerProtocol as pioProto, \
        PioneerFactory as pioFactory
from Modules.Housing.test.xml_housing import \
        TESTING_HOUSE_NAME, \
        TESTING_HOUSE_ACTIVE, \
        TESTING_HOUSE_KEY, \
        TESTING_HOUSE_UUID
from Modules.Housing.Entertainment.pioneer.test.xml_pioneer import \
        XML_PIONEER_SECTION, \
        TESTING_PIONEER_SECTION, \
        TESTING_PIONEER_DEVICE_NAME_0, \
        TESTING_PIONEER_DEVICE_KEY_0, \
        TESTING_PIONEER_DEVICE_ACTIVE_0, \
        TESTING_PIONEER_DEVICE_UUID_0, \
        TESTING_PIONEER_DEVICE_IPV4_0, \
        TESTING_PIONEER_DEVICE_PORT_0, \
        TESTING_PIONEER_DEVICE_NAME_1, \
        TESTING_PIONEER_DEVICE_KEY_1, \
        TESTING_PIONEER_DEVICE_ACTIVE_1, \
        TESTING_PIONEER_DEVICE_UUID_1, \
        TESTING_PIONEER_DEVICE_IPV4_1, \
        TESTING_PIONEER_DEVICE_PORT_1
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)

        self.m_factory = pioFactory(self.m_pyhouse_obj)
        self.m_transport = proto_helpers.StringTransport()
        self.m_proto = self.m_factory.buildProtocol(('127.0.0.1', 0))
        self.m_proto.makeConnection(self.m_transport)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_pioneer')


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
        self.assertIsNotNone(l_xml.find('PioneerSection'))

    def test_02_XmlTags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-02-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.entertainment_sect.tag, 'EntertainmentSection')
        self.assertEqual(self.m_xml.pioneer_sect.tag, 'PioneerSection')


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_PIONEER_SECTION
        print('A2-01-A - Raw', l_raw)
        self.assertEqual(l_raw[:16], '<PioneerSection>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_PIONEER_SECTION)
        print('A2-02-A - Parsed', l_xml)
        self.assertEqual(l_xml.tag, TESTING_PIONEER_SECTION)


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

    def test_03_PioneerXml(self):
        """ Test
        """
        l_xml = self.m_xml.pioneer_sect
        # print(PrettyFormatAny.form(l_xml, 'A3-03-A - Pioneer'))
        self.assertEqual(len(l_xml), 2)
        self.assertEqual(l_xml[0].attrib['Name'], TESTING_PIONEER_DEVICE_NAME_0)

    def test_04_Device0(self):
        """ Be sure that the XML contains everything in RoomData().
        """
        l_xml = self.m_xml.pioneer_sect.find('Device')
        # print(PrettyFormatAny.form(l_xml, 'A3-04-A Device'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_PIONEER_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_PIONEER_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_PIONEER_DEVICE_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_PIONEER_DEVICE_UUID_0)
        self.assertEqual(l_xml.find('IPv4').text, TESTING_PIONEER_DEVICE_IPV4_0)
        self.assertEqual(l_xml.find('Port').text, TESTING_PIONEER_DEVICE_PORT_0)


class B1_Read(SetupMixin, unittest.TestCase):
    """ Test that we read in the XML config properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_Device0(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj = pioneerXml._read_one(self.m_xml.pioneer_sect[0])
        # print(PrettyFormatAny.form(l_obj, 'B1-1-A - One Device'))
        self.assertEqual(l_obj.Name, TESTING_PIONEER_DEVICE_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_PIONEER_DEVICE_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_PIONEER_DEVICE_ACTIVE_0)
        self.assertEqual(l_obj.UUID, TESTING_PIONEER_DEVICE_UUID_0)
        # .
        self.assertEqual(convert.long_to_str(l_obj.IPv4), TESTING_PIONEER_DEVICE_IPV4_0)
        self.assertEqual(str(l_obj.Port), TESTING_PIONEER_DEVICE_PORT_0)

    def test_2_Device1(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj = pioneerXml._read_one(self.m_xml.pioneer_sect[1])
        # print(PrettyFormatAny.form(l_obj, 'B1-1-A - One Device'))
        self.assertEqual(l_obj.Name, TESTING_PIONEER_DEVICE_NAME_1)
        self.assertEqual(str(l_obj.Key), TESTING_PIONEER_DEVICE_KEY_1)
        self.assertEqual(str(l_obj.Active), TESTING_PIONEER_DEVICE_ACTIVE_1)
        self.assertEqual(l_obj.UUID, TESTING_PIONEER_DEVICE_UUID_1)
        # .
        self.assertEqual(convert.long_to_str(l_obj.IPv4), TESTING_PIONEER_DEVICE_IPV4_1)
        self.assertEqual(str(l_obj.Port), TESTING_PIONEER_DEVICE_PORT_1)

    def test_3_AllDevices(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj, _count = pioneerXml.read_all(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_obj[0], 'B1-2-A - All Devices'))
        print(PrettyFormatAny.form(l_obj[1], 'B1-2-B - All Devices'))
        self.assertEqual(l_obj.Name, TESTING_PIONEER_DEVICE_NAME_1)


class C1_Write(SetupMixin, unittest.TestCase):
    """ Test that we read in the XML config properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pioneer, _count = pioneerXml.read_all(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Pioneer = self.m_pioneer

    def test_1_Device0(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj = pioneerXml._read_one(self.m_xml.pioneer_sect[0])
        # print(PrettyFormatAny.form(l_obj, 'C1-1-A - One Device'))
        self.assertEqual(l_obj.Name, TESTING_PIONEER_DEVICE_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_PIONEER_DEVICE_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_PIONEER_DEVICE_ACTIVE_0)
        self.assertEqual(l_obj.UUID, TESTING_PIONEER_DEVICE_UUID_0)
        # .
        self.assertEqual(convert.long_to_str(l_obj.IPv4), TESTING_PIONEER_DEVICE_IPV4_0)
        self.assertEqual(str(l_obj.Port), TESTING_PIONEER_DEVICE_PORT_0)

    def test_2_Device1(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj = pioneerXml._read_one(self.m_xml.pioneer_sect[1])
        # print(PrettyFormatAny.form(l_obj, 'C1-2-A - One Device'))
        self.assertEqual(l_obj.Name, TESTING_PIONEER_DEVICE_NAME_1)
        self.assertEqual(str(l_obj.Key), TESTING_PIONEER_DEVICE_KEY_1)
        self.assertEqual(str(l_obj.Active), TESTING_PIONEER_DEVICE_ACTIVE_1)
        self.assertEqual(l_obj.UUID, TESTING_PIONEER_DEVICE_UUID_1)
        # .
        self.assertEqual(convert.long_to_str(l_obj.IPv4), TESTING_PIONEER_DEVICE_IPV4_1)
        self.assertEqual(str(l_obj.Port), TESTING_PIONEER_DEVICE_PORT_1)

    def test_3_AllDevices(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj = pioneerXml.read_all(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_obj, 'C2-3-A - All Devices'))
        l_xml = pioneerXml.write_all(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_xml, 'C2-3-B - All Devices'))

# ## END DBK
