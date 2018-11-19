"""
@name:      PyHouse/Project/src/Modules/Housing/Entertainment/test/test_entertainment_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Oct 17, 2018
@summary:   Test

Passed all 31 tests - DBK - 2018-11-13

"""

__updated__ = '2018-11-11'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from Modules.Core.Utilities import convert
from Modules.Core.Utilities.xml_tools import XmlConfigTools
from Modules.Housing.Entertainment.entertainment import API as entertainmentAPI
from Modules.Housing.Entertainment.entertainment_data import \
        EntertainmentData, \
        EntertainmentPluginData, \
        EntertainmentDeviceData, \
        EntertainmentServiceData
from Modules.Housing.Entertainment.entertainment_xml import XML as entertainmentXML
from Modules.Housing.Entertainment.onkyo.test.xml_onkyo import \
        TESTING_ONKYO_DEVICE_NAME_0, \
        TESTING_ONKYO_DEVICE_ACTIVE_0, \
        TESTING_ONKYO_DEVICE_KEY_0, \
        TESTING_ONKYO_DEVICE_COMMENT_0, \
        TESTING_ONKYO_DEVICE_NAME_1, \
        TESTING_ONKYO_DEVICE_ACTIVE_1, \
        TESTING_ONKYO_DEVICE_KEY_1, \
        TESTING_ONKYO_DEVICE_COMMENT_1, \
        TESTING_ONKYO_DEVICE_IPV4_0, \
        TESTING_ONKYO_DEVICE_IPV6_0, \
        TESTING_ONKYO_DEVICE_MODEL_0, \
        TESTING_ONKYO_DEVICE_ROOM_NAME_0, \
        TESTING_ONKYO_DEVICE_ROOM_UUID_0, \
        TESTING_ONKYO_DEVICE_TYPE_0, \
        TESTING_ONKYO_DEVICE_VOLUME_0, \
        TESTING_ONKYO_DEVICE_PORT_0, \
        TESTING_ONKYO_ACTIVE, \
        TESTING_ONKYO_DEVICE_COMMAND_SET_0, \
        TESTING_ONKYO_DEVICE_HOST_0, \
        TESTING_ONKYO_TYPE, \
        TESTING_ONKYO_DEVICE_UUID_0
from Modules.Housing.test.xml_housing import \
        TESTING_HOUSE_DIVISION, \
        TESTING_HOUSE_NAME, \
        TESTING_HOUSE_ACTIVE, \
        TESTING_HOUSE_KEY, \
        TESTING_HOUSE_UUID
from Modules.Housing.Entertainment.test.xml_entertainment import \
        TESTING_ENTERTAINMENT_SECTION, \
        XML_ENTERTAINMENT, \
        L_ENTERTAINMENT_SECTION_START
from Modules.Housing.Entertainment.pandora.test.xml_pandora import \
        TESTING_PANDORA_SECTION, \
        TESTING_PANDORA_DEVICE_NAME_0, \
        TESTING_PANDORA_DEVICE_ACTIVE_0, \
        TESTING_PANDORA_DEVICE_KEY_0, \
        TESTING_PANDORA_DEVICE_COMMENT_0, \
        TESTING_PANDORA_CONNECTION_DEVICE_FAMILY_0_0, \
        TESTING_PANDORA_CONNECTION_DEVICE_NAME_0_0, \
        TESTING_PANDORA_CONNECTION_DEFAULT_VOLUME_0_0, \
        TESTING_PANDORA_DEVICE_TYPE_0, \
        TESTING_PANDORA_DEVICE_MAX_PLAY_TIME_0, \
        TESTING_PANDORA_CONNECTION_INPUT_NAME_0_0, \
        TESTING_PANDORA_CONNECTION_INPUT_CODE_0_0, \
        TESTING_PANDORA_ACTIVE
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

BAD_TYPE = """
<PyHouse Version="18.7.0" Name="Test Computer">
    <HouseDivision>
        <EntertainmentSection>
            <JunkSection>
                <Type>Junk_type</Type>
            </JunkSection>
        </EntertainmentSection>
        <IrrigationSection />
    </HouseDivision>
</PyHouse>
"""


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = entertainmentAPI(self.m_pyhouse_obj)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_entertainment')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Tags'))
        self.assertEqual(self.m_pyhouse_obj.House.Rooms, {})

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
        l_raw = XML_ENTERTAINMENT
        # print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[:22], L_ENTERTAINMENT_SECTION_START)

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_ENTERTAINMENT)
        # print('A2-02-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'A2-02-A - Parsed')))
        self.assertEqual(l_xml.tag, TESTING_ENTERTAINMENT_SECTION)


class A3_XML(SetupMixin, unittest.TestCase):
    """ Now we test that the xml_xxxxx have set up the XML_LONG tree properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouseXML(self):
        """ Test to see if the house XML is built correctly
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Xml.XmlRoot, 'PyHouse'))
        pass

    def test_02_HouseDivXml(self):
        """ Test to see if the house XML is built correctly
        """
        l_xml = self.m_xml.house_div
        # print(PrettyFormatAny.form(l_xml, 'A3-02-A - House'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_HOUSE_NAME)
        self.assertEqual(l_xml.attrib['Active'], TESTING_HOUSE_ACTIVE)
        self.assertEqual(l_xml.attrib['Key'], TESTING_HOUSE_KEY)
        self.assertEqual(l_xml.find('UUID').text, TESTING_HOUSE_UUID)

    def test_03_EntertainmentXml(self):
        """ Test to see if the Entertainment XML is built properly
        """
        l_xml = self.m_xml.entertainment_sect
        # print(PrettyFormatAny.form(l_xml, 'A3-03-A - Entertainment'))
        # print(PrettyFormatAny.form(l_xml[1][0], 'A3-03-B - Entertainment'))
        self.assertEqual(l_xml.tag, TESTING_ENTERTAINMENT_SECTION)
        self.assertGreater(len(l_xml), 2)

    def test_04_EmptyEntertain(self):
        """ This will be sure the Entertainment portion of the PyHouse Object is empty
        """
        l_plugin = self.m_pyhouse_obj.House.Entertainment
        # print(PrettyFormatAny.form(l_plugin, 'A3-04-A - Entertainment'))
        self.assertEqual(l_plugin.Active, False)
        self.assertEqual(l_plugin.PluginCount, 0)
        self.assertEqual(l_plugin.Plugins, {})


class B1_Setup(SetupMixin, unittest.TestCase):
    """ This will test reading the onkyo devices as they are a part of the test suite.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(BAD_TYPE))
        self.m_xml = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection')

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Tags'))
        self.assertEqual(self.m_pyhouse_obj.House.Rooms, {})

    def test_02_Type(self):
        """ Test detecting bad type
        """
        l_xml = ET.fromstring(BAD_TYPE)
        # print(PrettyFormatAny.form(l_xml, 'B1-02-A - Bad XML'))
        l_ret = entertainmentXML().read_entertainment_subsection(l_xml)
        # print(PrettyFormatAny.form(l_ret, 'B1-02-B - Pandora Device'))
        self.assertEqual(l_ret.Type, 'Missing Type')


class C1_ReadDevice(SetupMixin, unittest.TestCase):
    """ This will test reading the onkyo devices as they are a part of the test suite.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_xml = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection')
        self.m_entertainment_obj = EntertainmentData()
        self.m_pyhouse_obj.House.Entertainment = EntertainmentData()  # Clear before loading
        self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'] = EntertainmentPluginData()

    def test_01_Setup(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_xml, 'C1-01-A - Entertainment XML'))
        self.assertEqual(self.m_xml.tag, TESTING_ENTERTAINMENT_SECTION)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'C1-01-B - Entertainment'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'], 'C1-01-C - Onkyo'))
        self.assertEqual(self.m_entertainment_obj.Active, False)
        self.assertEqual(self.m_entertainment_obj.PluginCount, 0)
        self.assertEqual(self.m_entertainment_obj.Plugins, {})

    def test_02_OneDevice0(self):
        """ Test that _create_module_refs is functional
        """
        l_xml = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection/OnkyoSection')
        l_xml = l_xml.findall('Device')[0]
        l_device = EntertainmentDeviceData()
        # print(PrettyFormatAny.form(l_xml, 'C1-02-A - Onkyo XML'))
        l_ret = entertainmentXML().read_entertainment_device(l_xml, l_device)
        # print(PrettyFormatAny.form(l_ret, 'C1-02-B - Onkyo Device'))
        self.assertEqual(l_ret.Name, TESTING_ONKYO_DEVICE_NAME_0)
        self.assertEqual(str(l_ret.Active), TESTING_ONKYO_DEVICE_ACTIVE_0)
        self.assertEqual(str(l_ret.Key), TESTING_ONKYO_DEVICE_KEY_0)
        self.assertEqual(str(l_ret.UUID), TESTING_ONKYO_DEVICE_UUID_0)
        self.assertEqual(l_ret.Comment, TESTING_ONKYO_DEVICE_COMMENT_0)
        self.assertEqual(l_ret.CommandSet, TESTING_ONKYO_DEVICE_COMMAND_SET_0)
        self.assertEqual(l_ret.Host, TESTING_ONKYO_DEVICE_HOST_0)
        self.assertEqual(convert.long_to_str(l_ret.IPv4), TESTING_ONKYO_DEVICE_IPV4_0)
        self.assertEqual(convert.long_to_str(l_ret.IPv6).lower(), TESTING_ONKYO_DEVICE_IPV6_0.lower())
        self.assertEqual(l_ret.Model, TESTING_ONKYO_DEVICE_MODEL_0)
        self.assertEqual(str(l_ret.Port), TESTING_ONKYO_DEVICE_PORT_0)
        self.assertEqual(l_ret.RoomName, TESTING_ONKYO_DEVICE_ROOM_NAME_0)
        self.assertEqual(l_ret.RoomUUID, TESTING_ONKYO_DEVICE_ROOM_UUID_0)
        self.assertEqual(l_ret.Type, TESTING_ONKYO_DEVICE_TYPE_0)
        self.assertEqual(str(l_ret.Volume), TESTING_ONKYO_DEVICE_VOLUME_0)

    def test_03_OneDevice1(self):
        """ Test
        """
        l_xml = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection/OnkyoSection')
        l_xml = l_xml.findall('Device')[1]
        l_device = EntertainmentDeviceData()
        # print(PrettyFormatAny.form(l_xml, 'C1-03-A - Onkyo XML'))
        l_ret = entertainmentXML().read_entertainment_device(l_xml, l_device)
        # print(PrettyFormatAny.form(l_ret, 'C1-03-B - Onkyo Device'))
        self.assertEqual(l_ret.Name, TESTING_ONKYO_DEVICE_NAME_1)
        self.assertEqual(str(l_ret.Active), TESTING_ONKYO_DEVICE_ACTIVE_1)
        self.assertEqual(str(l_ret.Key), TESTING_ONKYO_DEVICE_KEY_1)
        self.assertEqual(l_ret.Comment, TESTING_ONKYO_DEVICE_COMMENT_1)


class C2_ReadService(SetupMixin, unittest.TestCase):
    """
    This will test reading the pandora services as they are a part of the test suite.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_xml = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection')
        self.m_entertainment_obj = EntertainmentData()
        self.m_pyhouse_obj.House.Entertainment = EntertainmentData()  # Clear before loading
        self.m_pyhouse_obj.House.Entertainment.Plugins['pandora'] = EntertainmentPluginData()

    def test_01_Setup(self):
        """
        """
        l_xml = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection/PandoraSection')
        l_xml = l_xml.findall('Device')[0]
        l_service = EntertainmentServiceData()
        # print(PrettyFormatAny.form(self.m_xml, 'C2-01-A - Entertainment XML'))
        self.assertEqual(self.m_xml.tag, TESTING_ENTERTAINMENT_SECTION)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'C2-01-B - Entertainment'))
        self.assertEqual(self.m_entertainment_obj.Active, False)
        self.assertEqual(self.m_entertainment_obj.PluginCount, 0)
        self.assertEqual(self.m_entertainment_obj.Plugins, {})

    def test_02_OneDevice0(self):
        """ Test that _create_module_refs is functional
        """
        l_xml = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection/PandoraSection')
        l_xml = l_xml.findall('Device')[0]
        l_device = EntertainmentServiceData()
        # print(PrettyFormatAny.form(l_xml, 'C2-02-A - Pandora XML'))
        l_ret = entertainmentXML().read_entertainment_service(l_xml, l_device)
        # print(PrettyFormatAny.form(l_ret, 'C2-02-B - Pandora Service'))
        self.assertEqual(l_ret.Name, TESTING_PANDORA_DEVICE_NAME_0)
        self.assertEqual(str(l_ret.Active), TESTING_PANDORA_DEVICE_ACTIVE_0)
        self.assertEqual(str(l_ret.Key), TESTING_PANDORA_DEVICE_KEY_0)
        self.assertEqual(l_ret.Comment, TESTING_PANDORA_DEVICE_COMMENT_0)


class C3_ReadSubSection(SetupMixin, unittest.TestCase):
    """ This will test all of the sub modules ability to load their part of the XML file
            and this modules ability to put everything together in the structure
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_xml = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection')
        self.m_entertainment_obj = EntertainmentData()
        self.m_pyhouse_obj.House.Entertainment = EntertainmentData()  # Clear before loading

    def test_01_Setup(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_xml, 'C3-01-A - Entertainment XML'))
        self.assertEqual(self.m_xml.tag, TESTING_ENTERTAINMENT_SECTION)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'C3-01-B - Entertainment'))
        self.assertEqual(self.m_entertainment_obj.Active, False)
        self.assertEqual(self.m_entertainment_obj.PluginCount, 0)
        self.assertEqual(self.m_entertainment_obj.Plugins, {})

    def test_02_Onkyo(self):
        """ Test All of onkyo loads
        """
        l_xml = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection/OnkyoSection')
        # print(PrettyFormatAny.form(l_xml, 'C3-02-A - Onkyo XML'))
        l_ret = entertainmentXML().read_entertainment_subsection(l_xml)
        # print(PrettyFormatAny.form(l_ret, 'C3-02-B - Onkyo Plugin'))
        # print(PrettyFormatAny.form(l_ret.Devices, 'C3-02-C - Onkyo Devices'))
        self.assertEqual(l_ret.Active, TESTING_ONKYO_ACTIVE)
        self.assertEqual(l_ret.Name, 'onkyo')
        self.assertEqual(l_ret.Devices[0].Name, TESTING_ONKYO_DEVICE_NAME_0)
        self.assertEqual(str(l_ret.Devices[0].Active), TESTING_ONKYO_DEVICE_ACTIVE_0)
        self.assertEqual(str(l_ret.Devices[0].Key), TESTING_ONKYO_DEVICE_KEY_0)
        self.assertEqual(l_ret.Devices[0].Comment, TESTING_ONKYO_DEVICE_COMMENT_0)

    def test_03_Pandora(self):
        """
        """
        l_xml = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection/PandoraSection')
        # print(PrettyFormatAny.form(l_xml, 'C3-03-A - Pandora XML'))
        l_ret = entertainmentXML().read_entertainment_subsection(l_xml)
        # print(PrettyFormatAny.form(l_ret, 'C3-03-B - Pandora Plugin'))
        # print(PrettyFormatAny.form(l_ret.Services, 'C3-03-C - Pandora Services'))
        self.assertEqual(l_ret.Services[0].Name, TESTING_PANDORA_DEVICE_NAME_0)
        self.assertEqual(str(l_ret.Services[0].Active), TESTING_PANDORA_DEVICE_ACTIVE_0)
        self.assertEqual(str(l_ret.Services[0].Key), TESTING_PANDORA_DEVICE_KEY_0)
        self.assertEqual(l_ret.Services[0].Comment, TESTING_PANDORA_DEVICE_COMMENT_0)


class C4_ReadAll(SetupMixin, unittest.TestCase):
    """ This will test all of the sub modules ability to load their part of the XML file
            and this modules ability to put everything together in the structure
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_xml = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection')
        self.m_entertainment_obj = EntertainmentData()
        self.m_pyhouse_obj.House.Entertainment = EntertainmentData()  # Clear before loading

    def test_01_Setup(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_xml, 'C4-01-A - Entertainment XML'))
        self.assertEqual(self.m_xml.tag, TESTING_ENTERTAINMENT_SECTION)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'C4-01-B - Entertainment'))
        self.assertEqual(self.m_entertainment_obj.Active, False)
        self.assertEqual(self.m_entertainment_obj.PluginCount, 0)
        self.assertEqual(self.m_entertainment_obj.Plugins, {})

    def test_02_All(self):
        """
        """
        l_xml = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection')
        # print(PrettyFormatAny.form(l_xml, 'C4-02-A - Entertainment XML'))
        l_ret = entertainmentXML().read_entertainment_all(self.m_pyhouse_obj, l_xml)
        # print(PrettyFormatAny.form(l_ret, 'C4-02-B - Entertainment'))
        # print(PrettyFormatAny.form(l_ret.Plugins, 'C4-02-C - Plugins'))
        self.assertEqual(l_ret.Active, True)
        self.assertGreater(l_ret.PluginCount, 0)
        self.assertEqual(l_ret.Plugins['pandora'].Services[0].Name, TESTING_PANDORA_DEVICE_NAME_0)
        self.assertEqual(str(l_ret.Plugins['pandora'].Services[0].Active), TESTING_PANDORA_DEVICE_ACTIVE_0)
        self.assertEqual(str(l_ret.Plugins['pandora'].Services[0].Key), TESTING_PANDORA_DEVICE_KEY_0)
        self.assertEqual(l_ret.Plugins['pandora'].Services[0].Comment, TESTING_PANDORA_DEVICE_COMMENT_0)


class D1_WriteDevice(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_xml = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection')
        self.m_entertain = entertainmentXML().read_entertainment_all(self.m_pyhouse_obj, self.m_xml)
        self.m_pyhouse_obj.House.Entertainment = self.m_entertain

    def test_01_Setup(self):
        """ writing one onkyo device
        """
        # print(PrettyFormatAny.form(self.m_entertain, 'D1-01-A - Entertainment XML'))
        # print(PrettyFormatAny.form(self.m_entertain.Plugins, 'D1-01-B - Plugins'))
        # print(PrettyFormatAny.form(self.m_entertain.Plugins['onkyo'], 'D1-01-C - Onkyo'))
        self.assertEqual(self.m_xml.tag, TESTING_ENTERTAINMENT_SECTION)

    def test_02_Onko0(self):
        """ Test
        """
        l_xml = entertainmentXML().write_entertainment_device(self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'].Devices[0])
        # print(PrettyFormatAny.form(l_xml, 'D1-02-A - XML'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'D1-02-B - HouseInformation()'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ONKYO_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ONKYO_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ONKYO_DEVICE_ACTIVE_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_ONKYO_DEVICE_COMMENT_0)
        self.assertEqual(l_xml.find('IPv4').text, TESTING_ONKYO_DEVICE_IPV4_0)
        self.assertEqual(l_xml.find('IPv6').text.upper(), TESTING_ONKYO_DEVICE_IPV6_0.upper())
        self.assertEqual(l_xml.find('Model').text, TESTING_ONKYO_DEVICE_MODEL_0)
        self.assertEqual(l_xml.find('Port').text, TESTING_ONKYO_DEVICE_PORT_0)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_ONKYO_DEVICE_ROOM_NAME_0)
        self.assertEqual(l_xml.find('RoomUUID').text, TESTING_ONKYO_DEVICE_ROOM_UUID_0)
        self.assertEqual(l_xml.find('Type').text, TESTING_ONKYO_DEVICE_TYPE_0)
        self.assertEqual(l_xml.find('Volume').text, TESTING_ONKYO_DEVICE_VOLUME_0)

    def test_02_Onko1(self):
        """ Test
        """
        l_xml = entertainmentXML().write_entertainment_device(self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'].Devices[1])
        # print(PrettyFormatAny.form(l_xml, 'D1-02-A - Ret'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'D1-02-B - HouseInformation()'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ONKYO_DEVICE_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ONKYO_DEVICE_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ONKYO_DEVICE_ACTIVE_1)
        self.assertEqual(l_xml.find('Comment').text, TESTING_ONKYO_DEVICE_COMMENT_1)


class D2_WriteService(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_xml = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection')
        self.m_entertain = entertainmentXML().read_entertainment_all(self.m_pyhouse_obj, self.m_xml)
        self.m_pyhouse_obj.House.Entertainment = self.m_entertain

    def test_01_Pandora(self):
        """ Test
        """
        l_xml = entertainmentXML().write_entertainment_service(self.m_pyhouse_obj.House.Entertainment.Plugins['pandora'].Services[0])
        # print(PrettyFormatAny.form(l_xml, 'D2-01-A - XML'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'D2-01-B - HouseInformation()'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_PANDORA_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_PANDORA_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_PANDORA_DEVICE_ACTIVE_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_PANDORA_DEVICE_COMMENT_0)
        self.assertEqual(l_xml.find('ConnectionFamily').text, TESTING_PANDORA_CONNECTION_DEVICE_FAMILY_0_0)
        self.assertEqual(l_xml.find('ConnectionName').text, TESTING_PANDORA_CONNECTION_DEVICE_NAME_0_0)
        self.assertEqual(l_xml.find('InputCode').text, TESTING_PANDORA_CONNECTION_INPUT_CODE_0_0)
        self.assertEqual(l_xml.find('InputName').text, TESTING_PANDORA_CONNECTION_INPUT_NAME_0_0)
        self.assertEqual(l_xml.find('MaxPlayTime').text, TESTING_PANDORA_DEVICE_MAX_PLAY_TIME_0)
        self.assertEqual(l_xml.find('Type').text, TESTING_PANDORA_DEVICE_TYPE_0)
        self.assertEqual(l_xml.find('Volume').text, TESTING_PANDORA_CONNECTION_DEFAULT_VOLUME_0_0)


class D3_WriteSubSection(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_xml = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection')
        self.m_entertain = entertainmentXML().read_entertainment_all(self.m_pyhouse_obj, self.m_xml)
        self.m_pyhouse_obj.House.Entertainment = self.m_entertain

    def test_01_Component(self):
        """ Test
        """
        l_obj = self.m_entertain.Plugins['onkyo']
        # print(PrettyFormatAny.form(l_obj, 'D3-01-A - Onkyo'))
        # print(PrettyFormatAny.form(l_obj.Devices, 'D3-01-B - Devices'))
        # print(PrettyFormatAny.form(l_obj.Devices[0], 'D3-01-C - Drvice-0'))
        l_xml = entertainmentXML().write_entertainment_subsection(l_obj)
        print(PrettyFormatAny.form(l_xml, 'D3-01-F - XML'))
        self.assertEqual(l_xml.attrib['Active'], TESTING_ONKYO_ACTIVE)
        self.assertEqual(l_xml.find('Type').text, TESTING_ONKYO_TYPE)

    def test_02_Service(self):
        """ Test
        """
        l_xml = entertainmentXML().write_entertainment_subsection(self.m_entertain.Plugins['pandora'])
        # print(PrettyFormatAny.form(l_xml, 'D3-01-A - Ret'))
        # print(PrettyFormatAny.form(self.m_entertain.Plugins['pandora'], 'D3-01-B - Pandora'))
        self.assertEqual(l_xml.attrib['Active'], TESTING_PANDORA_ACTIVE)


class D4_WriteAll(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_xml = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection')
        self.m_entertain = entertainmentXML().read_entertainment_all(self.m_pyhouse_obj, self.m_xml)
        self.m_pyhouse_obj.House.Entertainment = self.m_entertain

    def test_01_Setup(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_xml, 'C1-01-A - Entertainment XML'))
        self.assertEqual(self.m_xml.tag, TESTING_ENTERTAINMENT_SECTION)

    def test_02_All(self):
        """
        """
        l_xml = entertainmentXML().write_entertainment_all(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_xml, 'D4-02-A - Entertainment XML'))
        self.assertEqual(self.m_xml.tag, TESTING_ENTERTAINMENT_SECTION)


class E1_Device(SetupMixin, unittest.TestCase):
    """ This will test reading the onkyo devices as they are a part of the test suite.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_xml = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection')
        self.m_entertainment_obj = EntertainmentData()
        self.m_pyhouse_obj.House.Entertainment = EntertainmentData()  # Clear before loading
        self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'] = EntertainmentPluginData()

    def test_01_Setup(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_xml, 'C1-01-A - Entertainment XML'))
        self.assertEqual(self.m_xml.tag, TESTING_ENTERTAINMENT_SECTION)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'C1-01-B - Entertainment'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'], 'C1-01-C - Onkyo'))
        self.assertEqual(self.m_entertainment_obj.Active, False)
        self.assertEqual(self.m_entertainment_obj.PluginCount, 0)

    def test_02_CreateModuleRefs(self):
        """ Test that _create_module_refs is functional
        """
        l_xml = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection/OnkyoSection')
        # print(PrettyFormatAny.form(l_xml, 'E1-02-A - Onkyo XML'))
        for l_section in self.m_xml:
            # print(PrettyFormatAny.form(l_section, 'E1-02-B - Section'))
            l_plug = self.m_api._create_module_refs(l_section)
            # print(PrettyFormatAny.form(l_plug, 'E1-02-B - One Plugin'))
            # self.m_pyhouse_obj.House.Entertainment.Plugins[l_plug.Name] = l_plug
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins, 'E1-02-C - Plugins'))
        # self.assertEqual(self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'].Device[0].Name, TESTING_ONKYO_DEVICE_NAME_0)
        pass

# ## END DBK
