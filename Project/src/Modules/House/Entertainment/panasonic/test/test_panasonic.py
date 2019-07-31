"""
@name:      PyHouse/src/Modules/Housing/Entertainment/panasonic/test/test_panasonic.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2018 by D. Brian Kimmel
@note:      Created on Aug 17, 2018
@license:   MIT License
@summary:

"""

__updated__ = '2019-06-30'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from Modules.Housing.Entertainment.panasonic.panasonic import XML as panasonicXML, SECTION
from Modules.Core.Utilities import convert
from Modules.Housing.Entertainment.entertainment_data import EntertainmentInformation, EntertainmentPluginInformation
from Modules.Housing.Entertainment.test.xml_entertainment import \
        TESTING_ENTERTAINMENT_SECTION
from Modules.Housing.Entertainment.panasonic.test.xml_panasonic import \
        TESTING_PANASONIC_DEVICE_UUID_0, \
        TESTING_PANASONIC_DEVICE_KEY_0, \
        TESTING_PANASONIC_DEVICE_NAME_0, \
        TESTING_PANASONIC_DEVICE_ACTIVE_0, \
        TESTING_PANASONIC_DEVICE_IPV4_0, \
        TESTING_PANASONIC_DEVICE_PORT_0, \
        TESTING_PANASONIC_DEVICE_COMMENT_0, \
        TESTING_PANASONIC_DEVICE_TYPE_0, \
        TESTING_PANASONIC_SECTION, \
        TESTING_PANASONIC_DEVICE_NAME_1, \
        TESTING_PANASONIC_DEVICE_KEY_1, \
        TESTING_PANASONIC_DEVICE_ACTIVE_1, \
        TESTING_PANASONIC_DEVICE_UUID_1, \
        TESTING_PANASONIC_DEVICE_VOLUME_0, \
        TESTING_PANASONIC_DEVICE_ROOM_NAME_0, \
        TESTING_PANASONIC_DEVICE_ROOM_UUID_0, \
        TESTING_PANASONIC_DEVICE_VOLUME_1, \
        XML_PANASONIC_SECTION, TESTING_PANASONIC_TYPE
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_pyhouse_obj.House.Entertainment = EntertainmentInformation()
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_panasonic')


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Objects(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_panasonic_xml = self.m_xml.entertainment_sect.find(TESTING_PANASONIC_SECTION)
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.entertainment_sect.tag, 'EntertainmentSection')
        self.assertEqual(l_panasonic_xml.tag, 'PanasonicSection')


class A2_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_PANASONIC_SECTION
        # print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[1:len(TESTING_PANASONIC_SECTION) + 1], TESTING_PANASONIC_SECTION)

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_PANASONIC_SECTION)
        print('A2-02-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'Parsed')))
        self.assertEqual(l_xml.tag, TESTING_PANASONIC_SECTION)


class A3_XML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by Panasonic.
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

    def test_02_Panasonic(self):
        """Ensure that the lighting objects are correct in the XML
        """
        l_xml = self.m_xml.entertainment_sect.find('PanasonicSection')
        # print(PrettyFormatAny.form(l_xml, 'A2-02-A - PyHouse'))
        self.assertEqual(l_xml.tag, TESTING_PANASONIC_SECTION)

    def test_03_Device0(self):
        """Ensure that the lighting objects are correct in the XML
        """
        l_xml = self.m_xml.panasonic_sect.findall('Device')[0]
        # print(PrettyFormatAny.form(l_xml, 'A2-03-A - PyHouse'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_PANASONIC_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_PANASONIC_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_PANASONIC_DEVICE_ACTIVE_0)

    def test_04_Device1(self):
        """Ensure that the lighting objects are correct in the XML
        """
        l_xml = self.m_xml.panasonic_sect.findall('Device')[1]
        # print(PrettyFormatAny.form(l_xml, 'A2-04-A - PyHouse'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_PANASONIC_DEVICE_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_PANASONIC_DEVICE_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_PANASONIC_DEVICE_ACTIVE_1)


class C1_Read(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the knko
        module can read/write.

    """

    def setUp(self):
        """ Set up the general PyHouse object, Entertainment, and panasonic structures
        """
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.Entertainment = EntertainmentInformation()
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginInformation()
        self.m_xml_panasonic = self.m_xml.entertainment_sect.find('PanasonicSection').find('Device')

    def test_01_base(self):
        """ Read one entire device entry and set up the PanasonicDeviceData_obj correctly.
        """
        l_xml = self.m_xml.entertainment_sect.find('PanasonicSection').find('Device')
        # print(PrettyFormatAny.form(l_xml, 'C1-01-A - XML Base Panasonic device.'))
        l_obj = panasonicXML._read_device(l_xml)
        # print(PrettyFormatAny.form(l_obj, 'C1-01-B - Base Panasonic device.'))
        # BaseUUID
        self.assertEqual(str(l_obj.Name), TESTING_PANASONIC_DEVICE_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_PANASONIC_DEVICE_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_PANASONIC_DEVICE_ACTIVE_0)
        self.assertEqual(str(l_obj.UUID), TESTING_PANASONIC_DEVICE_UUID_0)
        self.assertEqual(str(l_obj.Comment), TESTING_PANASONIC_DEVICE_COMMENT_0)
        # PanasonicDeviceData
        self.assertEqual(convert.long_to_str(l_obj.IPv4), TESTING_PANASONIC_DEVICE_IPV4_0)
        self.assertEqual(str(l_obj.Port), TESTING_PANASONIC_DEVICE_PORT_0)
        self.assertEqual(str(l_obj.RoomName), TESTING_PANASONIC_DEVICE_ROOM_NAME_0)
        self.assertEqual(str(l_obj.RoomUUID), TESTING_PANASONIC_DEVICE_ROOM_UUID_0)
        self.assertEqual(str(l_obj.Type), TESTING_PANASONIC_DEVICE_TYPE_0)
        self.assertEqual(str(l_obj.Volume), TESTING_PANASONIC_DEVICE_VOLUME_0)

    def test_02_One_0(self):
        """ Test first of multiple devices
        """
        l_xml = self.m_xml.panasonic_sect.findall('Device')[0]
        l_obj = panasonicXML._read_device(l_xml)
        # print(PrettyFormatAny.form(l_obj, 'C1-02-A - One Panasonic device.'))
        self.assertEqual(str(l_obj.Name), TESTING_PANASONIC_DEVICE_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_PANASONIC_DEVICE_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_PANASONIC_DEVICE_ACTIVE_0)
        self.assertEqual(str(l_obj.UUID), TESTING_PANASONIC_DEVICE_UUID_0)
        self.assertEqual(str(l_obj.Volume), TESTING_PANASONIC_DEVICE_VOLUME_0)

    def test_03_One_1(self):
        """ Test last of multiple devices
        """
        l_xml = self.m_xml.panasonic_sect.findall('Device')[1]
        l_obj = panasonicXML._read_device(l_xml)
        # print(PrettyFormatAny.form(l_obj, 'C1-03-A - One Panasonic device.'))
        self.assertEqual(str(l_obj.Name), TESTING_PANASONIC_DEVICE_NAME_1)
        self.assertEqual(str(l_obj.Key), TESTING_PANASONIC_DEVICE_KEY_1)
        self.assertEqual(str(l_obj.Active), TESTING_PANASONIC_DEVICE_ACTIVE_1)
        self.assertEqual(str(l_obj.UUID), TESTING_PANASONIC_DEVICE_UUID_1)
        self.assertEqual(str(l_obj.Volume), TESTING_PANASONIC_DEVICE_VOLUME_1)

    def test_04_All(self):
        """ test reading of entire device set.
        """
        l_obj = panasonicXML.read_panasonic_section_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_obj, 'C1-04-A - Plugins.'))
        print(PrettyFormatAny.form(l_obj.Devices, 'C1-04-B - Devices'))
        print(PrettyFormatAny.form(l_obj.Devices[0], 'C1-04-C - Device 0'))
        self.assertEqual(l_obj.Active, True)
        self.assertEqual(l_obj.DeviceCount, 2)
        self.assertEqual(str(l_obj.Devices[0].Name), TESTING_PANASONIC_DEVICE_NAME_0)
        self.assertEqual(str(l_obj.Devices[1].Name), TESTING_PANASONIC_DEVICE_NAME_1)

    def test_05_Data(self):
        """ test that the data structure is correct.
        """
        l_obj = panasonicXML.read_panasonic_section_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_obj, 'C1-05-A - Read'))
        l_base = self.m_pyhouse_obj.House.Entertainment
        print(PrettyFormatAny.form(l_base, 'C1-05-B1 - Base'))
        print(PrettyFormatAny.form(l_base.Plugins, 'C1-05-B2 - Plugins'))
        print(PrettyFormatAny.form(l_base.Plugins[SECTION], 'C1-05-B2 - Plugins[SECTION]'))
        self.assertEqual(l_obj.Type, TESTING_PANASONIC_TYPE)
        self.assertEqual(l_base.Plugins[SECTION].Name, SECTION)
        self.assertEqual(l_base.Plugins[SECTION].Devices[0].Name, TESTING_PANASONIC_DEVICE_NAME_0)
        self.assertEqual(l_base.Plugins[SECTION].Devices[1].Name, TESTING_PANASONIC_DEVICE_NAME_1)


class D1_Write(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local
        module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.Entertainment = EntertainmentInformation()
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginInformation()
        self.m_xml_panasonic = self.m_xml.entertainment_sect.find('PanasonicSection').find('Device')
        self.m_panasonic = panasonicXML.read_panasonic_section_xml(self.m_pyhouse_obj)

    def test_01_Data(self):
        """ test that the data structure is correct.
        """
        l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        print(PrettyFormatAny.form(l_base, 'C1-05-B1 - Base'))
        self.assertEqual(l_base.Type, TESTING_PANASONIC_TYPE)
        self.assertEqual(l_base.Name, SECTION)
        self.assertEqual(l_base.Devices[0].Name, TESTING_PANASONIC_DEVICE_NAME_0)
        self.assertEqual(l_base.Devices[1].Name, TESTING_PANASONIC_DEVICE_NAME_1)

    def test_02_Base(self):
        """Test the write for proper XML elements
        """
        # print(PrettyFormatAny.form(self.m_panasonic, 'D1-01-A - Plugin'))
        l_xml = panasonicXML._write_device(self.m_panasonic.Devices[0])
        print(PrettyFormatAny.form(l_xml, 'D1-01-B - XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_PANASONIC_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_PANASONIC_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_PANASONIC_DEVICE_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_PANASONIC_DEVICE_UUID_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_PANASONIC_DEVICE_COMMENT_0)
        #
        self.assertEqual(l_xml.find('IPv4').text, TESTING_PANASONIC_DEVICE_IPV4_0)
        self.assertEqual(l_xml.find('Port').text, TESTING_PANASONIC_DEVICE_PORT_0)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_PANASONIC_DEVICE_ROOM_NAME_0)
        self.assertEqual(l_xml.find('RoomUUID').text, TESTING_PANASONIC_DEVICE_ROOM_UUID_0)
        self.assertEqual(l_xml.find('Type').text, TESTING_PANASONIC_DEVICE_TYPE_0)
        self.assertEqual(l_xml.find('Volume').text, TESTING_PANASONIC_DEVICE_VOLUME_0)

    def test_03_One(self):
        """Test the write for proper XML elements
        """
        l_xml = panasonicXML._write_device(self.m_panasonic.Devices[0])
        # print(PrettyFormatAny.form(l_xml, 'D1-02-A - XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_PANASONIC_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_PANASONIC_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_PANASONIC_DEVICE_ACTIVE_0)

    def test_04_All(self):
        """Test the write for proper XML elements
        """
        l_xml = panasonicXML.write_panasonic_section_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_xml, 'D1-03-A - XML'))
        self.assertEqual(l_xml.find('Type').text, TESTING_PANASONIC_TYPE)
        self.assertEqual(l_xml[1].attrib['Name'], TESTING_PANASONIC_DEVICE_NAME_0)
        self.assertEqual(l_xml[1].attrib['Key'], TESTING_PANASONIC_DEVICE_KEY_0)
        self.assertEqual(l_xml[1].attrib['Active'], TESTING_PANASONIC_DEVICE_ACTIVE_0)
        self.assertEqual(l_xml[2].attrib['Name'], TESTING_PANASONIC_DEVICE_NAME_1)
        self.assertEqual(l_xml[2].attrib['Key'], TESTING_PANASONIC_DEVICE_KEY_1)
        self.assertEqual(l_xml[2].attrib['Active'], TESTING_PANASONIC_DEVICE_ACTIVE_1)


class E1_Load(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local
        module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.Entertainment = EntertainmentInformation()
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginInformation()
        self.m_xml_panasonic = self.m_xml.entertainment_sect.find('PanasonicSection').find('Device')
        self.m_panasonic = panasonicXML.read_panasonic_section_xml(self.m_pyhouse_obj)
        # self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]

    def test_01_Data(self):
        """ Test that the data is in the correct form
        """
        l_plugins = self.m_pyhouse_obj.House.Entertainment.Plugins
        print(PrettyFormatAny.form(l_plugins, 'E1-01-A - Plugins'))
        self.assertEqual(l_plugins['panasonic'].DeviceCount, 2)

    def test_03_Base(self):
        """Test the write for proper XML elements
        """
        l_obj = self.m_pyhouse_obj.House.Entertainment
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'E1-01-A - House'))
        print(PrettyFormatAny.form(l_obj, 'E1-01-B - Entertainment'))
        print(PrettyFormatAny.form(l_obj.Plugins, 'E1-01-C - Plugins'))
        print(PrettyFormatAny.form(l_obj.Plugins[SECTION], "E1-01-D - Plugins['panasonic]"))
        print(PrettyFormatAny.form(l_obj.Plugins[SECTION].Devices, "E1-01-E - Devices"))
        print(PrettyFormatAny.form(l_obj.Plugins[SECTION].Devices[0], "E1-01-F - Devices"))


class F1_Start(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local
        module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_panasonic = panasonicXML.read_panasonic_section_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Panasonic = self.m_panasonic

    def test_01_Base(self):
        """Test the write for proper XML elements
        """
        l_xml = panasonicXML._write_device(self.m_panasonic.Devices[0])


class G1_Save(SetupMixin, unittest.TestCase):
    """
    This section will verify the loaded Panasonic data will be saved properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_panasonic = panasonicXML.read_panasonic_section_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Panasonic = self.m_panasonic

    def test_01_Base(self):
        """Test the write for proper XML elements
        """
        l_xml = panasonicXML._write_device(self.m_panasonic.Devices[0])

# ## END DBK

# ## END DBK
