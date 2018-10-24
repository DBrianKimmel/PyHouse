"""
@name:      PyHouse/src/Modules/Housing/Entertainment/pioneer/test/test_pioneer.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 10, 2018
@summary:   Test

Passed all 18 tests - DBK - 2018-10-10

"""

__updated__ = '2018-10-17'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from twisted.test import proto_helpers

# Import PyMh files
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities import convert
from Modules.Housing.Entertainment.entertainment_data import \
        EntertainmentData, \
        EntertainmentPluginData
from Modules.Housing.Entertainment.pioneer.pioneer import \
        SECTION, \
        API as pioneerAPI, \
        XML as pioneerXml, \
        PioneerProtocol as pioProto, \
        PioneerFactory as pioFactory
from Modules.Housing.test.xml_housing import \
        TESTING_HOUSE_NAME, \
        TESTING_HOUSE_ACTIVE, \
        TESTING_HOUSE_KEY, \
        TESTING_HOUSE_UUID, TESTING_HOUSE_DIVISION
from Modules.Housing.Entertainment.test.xml_entertainment import \
        TESTING_ENTERTAINMENT_SECTION
from Modules.Housing.Entertainment.pioneer.test.xml_pioneer import \
        XML_PIONEER_SECTION, \
        L_PIONEER_SECTION_START, \
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
        TESTING_PIONEER_DEVICE_PORT_1, \
        TESTING_PIONEER_DEVICE_COMMAND_SET_0, \
        TESTING_PIONEER_DEVICE_ROOM_NAME_0, \
        TESTING_PIONEER_DEVICE_COMMENT_0, \
        TESTING_PIONEER_DEVICE_ROOM_UUID_0, \
        TESTING_PIONEER_DEVICE_STATUS_0, \
        TESTING_PIONEER_DEVICE_TYPE_0, \
        TESTING_PIONEER_DEVICE_VOLUME_0, \
        TESTING_PIONEER_ACTIVE
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)

    def setup2(self):
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
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)
        self.assertEqual(self.m_xml.entertainment_sect.tag, TESTING_ENTERTAINMENT_SECTION)
        self.assertEqual(self.m_xml.pioneer_sect.tag, TESTING_PIONEER_SECTION)


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_PIONEER_SECTION
        # print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[:16], L_PIONEER_SECTION_START[:16])

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_PIONEER_SECTION)
        # print('A2-02-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'Parsed')))
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
        self.assertEqual(self.m_xml.entertainment_sect.tag, TESTING_ENTERTAINMENT_SECTION)
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
        self.m_pyhouse_obj.House.Entertainment = EntertainmentData()
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        self.m_xml_pioneer = self.m_xml.pioneer_sect.find('Device')

    def test_01_Device(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj = pioneerXml._read_device(self.m_xml.pioneer_sect[0])
        # print(PrettyFormatAny.form(l_obj, 'B1-01-A - PioneerDeviceData'))
        self.assertEqual(l_obj.Name, TESTING_PIONEER_DEVICE_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_PIONEER_DEVICE_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_PIONEER_DEVICE_ACTIVE_0)
        self.assertEqual(str(l_obj.UUID), TESTING_PIONEER_DEVICE_UUID_0)
        self.assertEqual(str(l_obj.Comment), TESTING_PIONEER_DEVICE_COMMENT_0)
        self.assertEqual(str(l_obj.RoomName), TESTING_PIONEER_DEVICE_ROOM_NAME_0)
        self.assertEqual(l_obj.RoomUUID, TESTING_PIONEER_DEVICE_ROOM_UUID_0)
        # .
        self.assertEqual(convert.long_to_str(l_obj.IPv4), TESTING_PIONEER_DEVICE_IPV4_0)
        self.assertEqual(str(l_obj.Port), TESTING_PIONEER_DEVICE_PORT_0)
        self.assertEqual(str(l_obj.CommandSet), TESTING_PIONEER_DEVICE_COMMAND_SET_0)
        # self.assertEqual(str(l_obj.Status), TESTING_PIONEER_DEVICE_STATUS_0)
        self.assertEqual(str(l_obj.Type), TESTING_PIONEER_DEVICE_TYPE_0)
        self.assertEqual(str(l_obj.Volume), TESTING_PIONEER_DEVICE_VOLUME_0)

    def test_02_Device0(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj = pioneerXml._read_device(self.m_xml.pioneer_sect[0])
        # print(PrettyFormatAny.form(l_obj, 'B1-02-A - One Device'))
        self.assertEqual(l_obj.Name, TESTING_PIONEER_DEVICE_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_PIONEER_DEVICE_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_PIONEER_DEVICE_ACTIVE_0)
        self.assertEqual(str(l_obj.UUID), TESTING_PIONEER_DEVICE_UUID_0)
        self.assertEqual(str(l_obj.Comment), TESTING_PIONEER_DEVICE_COMMENT_0)
        self.assertEqual(str(l_obj.RoomName), TESTING_PIONEER_DEVICE_ROOM_NAME_0)
        self.assertEqual(l_obj.RoomUUID, TESTING_PIONEER_DEVICE_ROOM_UUID_0)
        # .
        self.assertEqual(convert.long_to_str(l_obj.IPv4), TESTING_PIONEER_DEVICE_IPV4_0)
        self.assertEqual(str(l_obj.Port), TESTING_PIONEER_DEVICE_PORT_0)
        self.assertEqual(str(l_obj.CommandSet), TESTING_PIONEER_DEVICE_COMMAND_SET_0)
        # self.assertEqual(str(l_obj.Status), TESTING_PIONEER_DEVICE_STATUS_0)
        self.assertEqual(str(l_obj.Type), TESTING_PIONEER_DEVICE_TYPE_0)
        self.assertEqual(str(l_obj.Volume), TESTING_PIONEER_DEVICE_VOLUME_0)

    def test_03_Device1(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj = pioneerXml._read_device(self.m_xml.pioneer_sect[1])
        # print(PrettyFormatAny.form(l_obj, 'B1-03-A - One Device'))
        self.assertEqual(l_obj.Name, TESTING_PIONEER_DEVICE_NAME_1)
        self.assertEqual(str(l_obj.Key), TESTING_PIONEER_DEVICE_KEY_1)
        self.assertEqual(str(l_obj.Active), TESTING_PIONEER_DEVICE_ACTIVE_1)
        self.assertEqual(l_obj.UUID, TESTING_PIONEER_DEVICE_UUID_1)
        # .
        self.assertEqual(convert.long_to_str(l_obj.IPv4), TESTING_PIONEER_DEVICE_IPV4_1)
        self.assertEqual(str(l_obj.Port), TESTING_PIONEER_DEVICE_PORT_1)

    def test_04_AllDevices(self):
        """ Read the xml and fill in the first room's dict
        """
        l_obj = pioneerXml.read_pioneer_section_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'B1-04-A - All Devices'))
        # print(PrettyFormatAny.form(l_obj.Devices, 'B1-04-B - Devices'))
        # print(PrettyFormatAny.form(l_obj.Devices[0], 'B1-04-C - Device[0]'))
        self.assertEqual(l_obj.Count, 2)
        self.assertEqual(str(l_obj.Active), TESTING_PIONEER_ACTIVE)
        self.assertEqual(l_obj.Devices[0].Name, TESTING_PIONEER_DEVICE_NAME_0)
        self.assertEqual(l_obj.Devices[1].Name, TESTING_PIONEER_DEVICE_NAME_1)


class D1_Write(SetupMixin, unittest.TestCase):
    """ Test that we write out the xml properly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.Entertainment = EntertainmentData()
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        self.m_section = pioneerXml.read_pioneer_section_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Pioneer = self.m_section

    def test_01_Setup(self):
        """ Write the XML for a device
        """
        print(PrettyFormatAny.form(self.m_section, 'D1-01-A - Section'))
        print(PrettyFormatAny.form(self.m_section.Devices[0], 'D1-01-A - Section'))
        print(PrettyFormatAny.form(self.m_section.Devices[1], 'D1-01-A - Section'))

        # print(PrettyFormatAny.form(l_xml, 'D1-01-B - One Device'))
    def test_02_Device(self):
        """ Write the XML for a device
        """
        l_obj = pioneerXml._read_device(self.m_xml.pioneer_sect[0])
        # print(PrettyFormatAny.form(l_obj, 'D1-01-A - One Device'))
        l_xml = pioneerXml._write_device(l_obj)
        # print(PrettyFormatAny.form(l_xml, 'D1-01-B - One Device'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_PIONEER_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_PIONEER_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_PIONEER_DEVICE_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_PIONEER_DEVICE_UUID_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_PIONEER_DEVICE_COMMENT_0)
        #
        self.assertEqual(l_xml.find('IPv4').text, TESTING_PIONEER_DEVICE_IPV4_0)

    def test_03_Device0(self):
        """ Write
        """
        l_obj = pioneerXml._read_device(self.m_xml.pioneer_sect[0])
        # print(PrettyFormatAny.form(l_obj, 'D1-02-A - One Device'))
        l_xml = pioneerXml._write_device(l_obj)
        # print(PrettyFormatAny.form(l_xml, 'D1-02-B - One Device'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_PIONEER_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_PIONEER_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_PIONEER_DEVICE_ACTIVE_0)

    def test_04_Device1(self):
        """ Write
        """
        l_obj = pioneerXml._read_device(self.m_xml.pioneer_sect[1])
        # print(PrettyFormatAny.form(l_obj, 'D1-03-A - One Device'))
        l_xml = pioneerXml._write_device(l_obj)
        # print(PrettyFormatAny.form(l_xml, 'D1-03-B - One Device'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_PIONEER_DEVICE_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_PIONEER_DEVICE_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_PIONEER_DEVICE_ACTIVE_1)

    def test_05_AllDevices(self):
        """ Write
        """
        l_obj = pioneerXml.read_pioneer_section_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = l_obj
        # print(PrettyFormatAny.form(l_obj, 'D1-04-A - EntertainmentPluginData'))
        l_xml = pioneerXml.write_pioneer_section_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'D1-04-B - All Devices'))


class E1_API(SetupMixin, unittest.TestCase):
    """ Test that we write out the xml properly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.Entertainment = EntertainmentData()
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        self.m_pioneer = pioneerXml.read_pioneer_section_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Pioneer = self.m_pioneer
        self.m_api = pioneerAPI(self.m_pyhouse_obj)

    def test_01_Find(self):
        """ Find the correct device obj
        """
        l_family = 'pioneer'
        l_device = '822-k'
        l_dev_obj = self.m_api._find_device(l_family, l_device)
        # print(PrettyFormatAny.form(l_dev_obj, 'E1-01-A - All Devices'))
        # print(PrettyFormatAny.form(self.m_api, 'E1-01-B - API'))
        self.assertEqual(l_dev_obj.Name, TESTING_PIONEER_DEVICE_NAME_0)

# ## END DBK
