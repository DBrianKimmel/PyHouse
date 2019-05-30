"""
@name: PyHouse/Project/src/Modules/Housing/Entertainment/pandora/test/test_pandora_xml.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: (c)2019-2019 by D. Brian Kimmel
@note: Created on Apr 15, 2019
@license: MIT License
@summary: Loads/Saves extra pandora info from XML file.

Passed all 15 tests - DBK - 2019-04-20

"""

__updated__ = '2019-05-29'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Housing.Entertainment.pandora.pandora import SECTION
from Modules.Housing.Entertainment.pandora.pandora_xml import XML as pandoraXML
from Modules.Housing.Entertainment.pandora.test.xml_pandora import \
    TESTING_PANDORA_SECTION, \
    XML_PANDORA_SECTION, \
    L_PANDORA_SECTION_START, \
    TESTING_PANDORA_SERVICE_NAME_0, \
    TESTING_PANDORA_SERVICE_KEY_0, \
    TESTING_PANDORA_SERVICE_ACTIVE_0, \
    TESTING_PANDORA_SERVICE_COMMENT_0, \
    TESTING_PANDORA_SERVICE_HOST_0, \
    TESTING_PANDORA_SERVICE_TYPE_0, \
    TESTING_PANDORA_ACTIVE, \
    TESTING_PANDORA_CONNECTION_DEVICE_FAMILY_0_0, \
    TESTING_PANDORA_CONNECTION_DEVICE_MODEL_0_0, \
    TESTING_PANDORA_CONNECTION_INPUT_NAME_0_0, \
    TESTING_PANDORA_CONNECTION_INPUT_CODE_0_0, \
    TESTING_PANDORA_SERVICE_MAX_PLAY_TIME_0, \
    TESTING_PANDORA_CONNECTION_DEFAULT_VOLUME_0_0, \
    TESTING_PANDORA_TYPE, TESTING_PANDORA_MAX_SESSIONS
from Modules.Housing.test.xml_housing import \
    TESTING_HOUSE_DIVISION, \
    TESTING_HOUSE_NAME, \
    TESTING_HOUSE_ACTIVE, \
    TESTING_HOUSE_KEY, \
    TESTING_HOUSE_UUID
from Modules.Housing.Entertainment.test.xml_entertainment import \
    TESTING_ENTERTAINMENT_SECTION
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Housing.Entertainment.entertainment_data import EntertainmentData, EntertainmentPluginData
from Modules.Core.Utilities import convert


class SetupMixin:

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_pandora_xml')


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
        """ Be sure that the XML contains the right tag information.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-02-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)
        self.assertEqual(self.m_xml.entertainment_sect.tag, TESTING_ENTERTAINMENT_SECTION)
        self.assertEqual(self.m_xml.pandora_sect.tag, TESTING_PANDORA_SECTION)


class A2_SetupXml(SetupMixin, unittest.TestCase):
    """ Test that the XML contains no syntax errors.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))

    def test_01_Raw(self):
        l_raw = XML_PANDORA_SECTION
        l_len = len(TESTING_PANDORA_SECTION) + 1  # leading '<'
        # print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[:l_len], L_PANDORA_SECTION_START[:l_len])

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_PANDORA_SECTION)
        # print('A2-02-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'A2-02-A - Parsed')))
        self.assertEqual(l_xml.tag, TESTING_PANDORA_SECTION)


class A3_XML(SetupMixin, unittest.TestCase):
    """ Now we test that the xml_xxxxx have set up the XML_LONG tree properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_HouseDivXml(self):
        """ Test the XML for a proper 'HouseDivision'
        """
        l_xml = self.m_xml.house_div
        # print(PrettyFormatAny.form(l_xml, 'A3-01-A - House'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_HOUSE_NAME)
        self.assertEqual(l_xml.attrib['Active'], TESTING_HOUSE_ACTIVE)
        self.assertEqual(l_xml.attrib['Key'], TESTING_HOUSE_KEY)
        self.assertEqual(l_xml.find('UUID').text, TESTING_HOUSE_UUID)

    def test_02_EntertainmentXml(self):
        """ Test if the number of Entertainment sub sections is correct.
        """
        l_xml = self.m_xml.entertainment_sect
        # print(PrettyFormatAny.form(l_xml, 'A3-02-A - Entertainment'))
        self.assertEqual(len(l_xml), 5)

    def test_03_PandoraXml(self):
        """ Test the pandora section
        """
        l_xml = self.m_xml.pandora_sect
        # print(PrettyFormatAny.form(l_xml, 'A3-03-A - Pandora'))
        self.assertEqual(len(l_xml), 3)
        self.assertEqual(l_xml[2].attrib['Name'], TESTING_PANDORA_SERVICE_NAME_0)

    def test_04_Device0(self):
        """ Be sure that the XML contains everything in RoomData().
        """
        l_xml = self.m_xml.pandora_sect.find('Service')
        # print(PrettyFormatAny.form(l_xml, 'A3-04-A Device'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_PANDORA_SERVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_PANDORA_SERVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_PANDORA_SERVICE_ACTIVE_0)


class C1_Read(SetupMixin, unittest.TestCase):
    """ Test that we read in the XML configuration properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.Entertainment = EntertainmentData()
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        self.m_xml_pandora = self.m_xml.pandora_sect.find('Service')

    def test_01_Build(self):
        """ Read one entire device entry and set up the PandoraDeviceData_obj correctly.
        """
        l_obj = pandoraXML()._read_pandora_base(self.m_xml_pandora)
        # sprint(PrettyFormatAny.form(l_obj, 'C1-01-B - Base Pandora device.'))
        # Base
        self.assertEqual(str(l_obj.Name), TESTING_PANDORA_SERVICE_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_PANDORA_SERVICE_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_PANDORA_SERVICE_ACTIVE_0)
        self.assertEqual(str(l_obj.Comment), TESTING_PANDORA_SERVICE_COMMENT_0)
        # OnkyoDeviceData
        self.assertEqual(convert.long_to_str(l_obj.Host), TESTING_PANDORA_SERVICE_HOST_0)
        self.assertEqual(str(l_obj.ConnectionFamily), TESTING_PANDORA_CONNECTION_DEVICE_FAMILY_0_0)
        self.assertEqual(str(l_obj.ConnectionModel), TESTING_PANDORA_CONNECTION_DEVICE_MODEL_0_0)
        self.assertEqual(str(l_obj.InputName), TESTING_PANDORA_CONNECTION_INPUT_NAME_0_0)
        self.assertEqual(str(l_obj.MaxPlayTime), TESTING_PANDORA_SERVICE_MAX_PLAY_TIME_0)
        self.assertEqual(str(l_obj.Volume), TESTING_PANDORA_CONNECTION_DEFAULT_VOLUME_0_0)

    def test_02_Base(self):
        """  Read the Pandora base section.
        """
        l_obj = pandoraXML()._read_pandora_base(self.m_xml_pandora)
        print(PrettyFormatAny.form(l_obj, 'C1-02-B - One Device'))
        self.assertEqual(l_obj.Name, TESTING_PANDORA_SERVICE_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_PANDORA_SERVICE_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_PANDORA_SERVICE_ACTIVE_0)
        # .
        self.assertEqual(convert.long_to_str(l_obj.Host), TESTING_PANDORA_SERVICE_HOST_0)

    def test_03_AllServices(self):
        """ Read all the pandora devices
        """
        l_obj = pandoraXML().read_pandora_section_xml(self.m_pyhouse_obj)
        l_ent = self.m_pyhouse_obj.House.Entertainment
        print(PrettyFormatAny.form(l_obj, 'C1-03-B - All Services'))
        print(PrettyFormatAny.form(l_obj.Services, 'C1-03-C - All Services'))
        print(PrettyFormatAny.form(l_obj.Services[0], 'C1-03-D - Service-0'))
        # print(PrettyFormatAny.form(l_ent, 'C1-03-H - Entertainment'))
        # print(PrettyFormatAny.form(l_ent.Plugins[SECTION], "B1-03-I - Plugins['pandora']"))
        # print(PrettyFormatAny.form(l_ent.Plugins[SECTION].Devices, "B1-03-J - Plugins['pandora'],Devices"))
        # print(PrettyFormatAny.form(l_ent.Plugins[SECTION].Devices[0], "B1-03-K - Plugins['pandora'],Devices[0]"))
        self.assertEqual(l_ent.Plugins[SECTION].Services[0].Name, TESTING_PANDORA_SERVICE_NAME_0)
        self.assertEqual(str(l_obj.Type), TESTING_PANDORA_SERVICE_TYPE_0)
        self.assertEqual(str(l_obj.Active), TESTING_PANDORA_ACTIVE)
        self.assertEqual(str(l_obj.MaxSessions), TESTING_PANDORA_MAX_SESSIONS)


class D1_Write(SetupMixin, unittest.TestCase):
    """ Test that we write XML correctly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.Entertainment = EntertainmentData()
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        self.m_xml_pandora = self.m_xml.entertainment_sect.find('PandoraSection').find('Device')
        self.m_pandora = pandoraXML().read_pandora_section_xml(self.m_pyhouse_obj)

    def test_01_Data(self):
        """ Test that the Pandora data structure was built correctly.
        """
        l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'D1-01-A - Entertainment'))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins, 'D1-01-B - Plugins'))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION], 'D1-01-C - Pandora'))
        print(PrettyFormatAny.form(l_base, 'D1-01-G - Base'))
        self.assertEqual(l_base.Type, TESTING_PANDORA_TYPE)
        self.assertEqual(l_base.Name, SECTION)
        self.assertEqual(str(l_base.MaxSessions), TESTING_PANDORA_MAX_SESSIONS)
        self.assertEqual(l_base.Services[0].Name, TESTING_PANDORA_SERVICE_NAME_0)

    def test_02_OneDevice(self):
        """ Test the write for proper XML elements.
        """
        l_xml = pandoraXML()._write_service(self.m_pandora.Services[0])
        # print(PrettyFormatAny.form(l_xml, 'D1-02-A - XML'))
        # Base
        self.assertEqual(l_xml.attrib['Name'], TESTING_PANDORA_SERVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_PANDORA_SERVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_PANDORA_SERVICE_ACTIVE_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_PANDORA_SERVICE_COMMENT_0)
        # EntertainmentServiceData
        self.assertEqual(l_xml.find('Host').text, TESTING_PANDORA_SERVICE_HOST_0)
        self.assertEqual(l_xml.find('MaxPlayTime').text, TESTING_PANDORA_SERVICE_MAX_PLAY_TIME_0)
        self.assertEqual(l_xml.find('ConnectionModel').text, TESTING_PANDORA_CONNECTION_DEVICE_MODEL_0_0)
        self.assertEqual(l_xml.find('InputName').text, TESTING_PANDORA_CONNECTION_INPUT_NAME_0_0)
        self.assertEqual(l_xml.find('Volume').text, TESTING_PANDORA_CONNECTION_DEFAULT_VOLUME_0_0)

    def test_03_Base(self):
        """ Write the entire PandoraSection XML
        """
        l_xml = pandoraXML().write_pandora_section_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'D1-03-A - All Devices'))
        self.assertEqual(l_xml.attrib['Active'], TESTING_PANDORA_ACTIVE)
        self.assertEqual(l_xml.find('Type').text, TESTING_PANDORA_SERVICE_TYPE_0)
        self.assertEqual(l_xml.find('MaxSessions').text, TESTING_PANDORA_MAX_SESSIONS)

    def test_04_All(self):
        """ Write the entire PandoraSection XML
        """
        l_xml = pandoraXML().write_pandora_section_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_xml, 'D1-04-A - All Devices'))

# ## END DBK
