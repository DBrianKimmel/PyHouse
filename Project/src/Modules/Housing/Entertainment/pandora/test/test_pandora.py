"""
@name:      PyHouse/src/Modules/entertain/test/test_pandora.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 22, 2014
@summary:   Test

Passed all 26 tests - DBK - 2018-10-25

"""

__updated__ = '2018-12-27'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities import convert
from Modules.Housing.Entertainment.entertainment import API as entertainmentAPI
from Modules.Housing.Entertainment.pandora.pandora import \
        XML as pandoraXml, \
        API as pandoraAPI, \
        SECTION, \
        MqttActions, PianoBarProcessControl, PandoraStatusData
from Modules.Housing.Entertainment.pandora.test.xml_pandora import \
        XML_PANDORA_SECTION, \
        TESTING_PANDORA_SECTION, \
        L_PANDORA_SECTION_START, \
        TESTING_PANDORA_DEVICE_NAME_0, \
        TESTING_PANDORA_DEVICE_KEY_0, \
        TESTING_PANDORA_DEVICE_ACTIVE_0, \
        TESTING_PANDORA_DEVICE_HOST_0, \
        TESTING_PANDORA_DEVICE_TYPE_0, \
        TESTING_PANDORA_DEVICE_COMMENT_0, \
        TESTING_PANDORA_CONNECTION_DEFAULT_VOLUME_0_0, \
        TESTING_PANDORA_CONNECTION_DEVICE_NAME_0_0, \
        TESTING_PANDORA_CONNECTION_DEVICE_FAMILY_0_0, \
        TESTING_PANDORA_CONNECTION_INPUT_NAME_0_0, \
        TESTING_PANDORA_CONNECTION_INPUT_CODE_0_0, \
        TESTING_PANDORA_TYPE, \
        TESTING_PANDORA_DEVICE_MAX_PLAY_TIME_0, \
        TESTING_PANDORA_ACTIVE
from Modules.Housing.test.xml_housing import \
        TESTING_HOUSE_DIVISION, \
        TESTING_HOUSE_NAME, \
        TESTING_HOUSE_ACTIVE, \
        TESTING_HOUSE_KEY, \
        TESTING_HOUSE_UUID
from Modules.Housing.Entertainment.entertainment_data import \
        EntertainmentData, \
        EntertainmentPluginData
from Modules.Housing.Entertainment.test.xml_entertainment import \
        TESTING_ENTERTAINMENT_SECTION
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

CTL = {
    'Sender' : 'Computer_1',
    'Control': 'PowerOff'
    }

TIME_LN = b'#   -03:00/03:00\r'
PLAY_LN = b'   "Love Is On The Way" by "Dave Koz" on "Greatest Hits" <3 @ Smooth Jazz Radio'


class SetupMixin:

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


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


class A2_SetupXml(SetupMixin, unittest.TestCase):
    """ Test that the XML contains no syntax errors.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_PANDORA_SECTION
        # print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[:16], L_PANDORA_SECTION_START[:16])

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
        """ Test if the number of sub sections is the same as configured in the XML
        """
        l_xml = self.m_xml.entertainment_sect
        # print(PrettyFormatAny.form(l_xml, 'A3-02-A - Entertainment'))
        self.assertGreater(len(l_xml), 0)

    def test_03_PandoraXml(self):
        """ Test
        """
        l_xml = self.m_xml.pandora_sect
        # print(PrettyFormatAny.form(l_xml, 'A3-03-A - Pandora'))
        self.assertEqual(len(l_xml), 2)
        self.assertEqual(l_xml[1].attrib['Name'], TESTING_PANDORA_DEVICE_NAME_0)

    def test_04_Device0(self):
        """ Be sure that the XML contains everything in RoomData().
        """
        l_xml = self.m_xml.pandora_sect.find('Device')
        # print(PrettyFormatAny.form(l_xml, 'A3-04-A Device'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_PANDORA_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_PANDORA_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_PANDORA_DEVICE_ACTIVE_0)


class C1_Read(SetupMixin, unittest.TestCase):
    """ Test that we read in the XML configuration properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.Entertainment = EntertainmentData()
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        self.m_xml_pandora = self.m_xml.pandora_sect.find('Device')

    def test_01_Build(self):
        """ Read one entire device entry and set up the PandoraDeviceData_obj correctly.
        """
        l_obj = pandoraXml._read_device(self.m_xml_pandora)
        # sprint(PrettyFormatAny.form(l_obj, 'C1-01-B - Base Pandora device.'))
        # Base
        self.assertEqual(str(l_obj.Name), TESTING_PANDORA_DEVICE_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_PANDORA_DEVICE_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_PANDORA_DEVICE_ACTIVE_0)
        self.assertEqual(str(l_obj.Comment), TESTING_PANDORA_DEVICE_COMMENT_0)
        # OnkyoDeviceData
        self.assertEqual(convert.long_to_str(l_obj.Host), TESTING_PANDORA_DEVICE_HOST_0)
        self.assertEqual(str(l_obj.ConnectionFamily), TESTING_PANDORA_CONNECTION_DEVICE_FAMILY_0_0)
        self.assertEqual(str(l_obj.ConnectionName), TESTING_PANDORA_CONNECTION_DEVICE_NAME_0_0)
        self.assertEqual(str(l_obj.InputName), TESTING_PANDORA_CONNECTION_INPUT_NAME_0_0)
        self.assertEqual(str(l_obj.InputCode), TESTING_PANDORA_CONNECTION_INPUT_CODE_0_0)
        self.assertEqual(str(l_obj.MaxPlayTime), TESTING_PANDORA_DEVICE_MAX_PLAY_TIME_0)
        self.assertEqual(str(l_obj.Volume), TESTING_PANDORA_CONNECTION_DEFAULT_VOLUME_0_0)

    def test_02_OneDevice(self):
        """  Read the first Pandora device.
        """
        l_obj = pandoraXml._read_device(self.m_xml_pandora)
        # print(PrettyFormatAny.form(l_obj, 'C1-02-B - One Device'))
        self.assertEqual(l_obj.Name, TESTING_PANDORA_DEVICE_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_PANDORA_DEVICE_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_PANDORA_DEVICE_ACTIVE_0)
        # .
        self.assertEqual(convert.long_to_str(l_obj.Host), TESTING_PANDORA_DEVICE_HOST_0)

    def test_03_AllDevices(self):
        """ Read all the pandora devices
        """
        l_obj = pandoraXml.read_pandora_section_xml(self.m_pyhouse_obj)
        l_ent = self.m_pyhouse_obj.House.Entertainment
        # print(PrettyFormatAny.form(_l_obj, 'C1-03-B - All Devices'))
        # print(PrettyFormatAny.form(_l_obj.Devices, 'C1-03-C - All Devices'))
        # print(PrettyFormatAny.form(_l_obj.Devices[0], 'C1-03-D - All Devices'))
        # print(PrettyFormatAny.form(l_ent, 'C1-03-H - Entertainment'))
        # print(PrettyFormatAny.form(l_ent.Plugins[SECTION], "B1-03-I - Plugins['pandora']"))
        # print(PrettyFormatAny.form(l_ent.Plugins[SECTION].Devices, "B1-03-J - Plugins['pandora'],Devices"))
        # print(PrettyFormatAny.form(l_ent.Plugins[SECTION].Devices[0], "B1-03-K - Plugins['pandora'],Devices[0]"))
        self.assertEqual(l_ent.Plugins[SECTION].Devices[0].Name, TESTING_PANDORA_DEVICE_NAME_0)
        self.assertEqual(str(l_obj.Type), TESTING_PANDORA_DEVICE_TYPE_0)
        self.assertEqual(str(l_obj.Active), TESTING_PANDORA_ACTIVE)


class D1_Write(SetupMixin, unittest.TestCase):
    """ Test that we write XML correctly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.Entertainment = EntertainmentData()
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        self.m_xml_pandora = self.m_xml.entertainment_sect.find('PandoraSection').find('Device')
        self.m_pandora = pandoraXml.read_pandora_section_xml(self.m_pyhouse_obj)

    def test_01_Data(self):
        """ Test that the data structure is correct.
        """
        l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'D1-01-A1 - PyHouse'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'D1-01-A2 - House'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'D1-01-A3 - Entertainment'))
        # print(PrettyFormatAny.form(l_base, 'C1-05-B1 - Base'))
        self.assertEqual(l_base.Type, TESTING_PANDORA_TYPE)
        self.assertEqual(l_base.Name, SECTION)
        self.assertEqual(l_base.Devices[0].Name, TESTING_PANDORA_DEVICE_NAME_0)

    def test_02_OneDevice(self):
        """ TTest the write for proper XML elements.
        """
        l_xml = pandoraXml._write_device(self.m_pandora.Devices[0])
        # print(PrettyFormatAny.form(l_xml, 'D1-02-A - XML'))
        # Base
        self.assertEqual(l_xml.attrib['Name'], TESTING_PANDORA_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_PANDORA_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_PANDORA_DEVICE_ACTIVE_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_PANDORA_DEVICE_COMMENT_0)
        # EntertainmentServiceData
        self.assertEqual(l_xml.find('Host').text, TESTING_PANDORA_DEVICE_HOST_0)
        self.assertEqual(l_xml.find('MaxPlayTime').text, TESTING_PANDORA_DEVICE_MAX_PLAY_TIME_0)
        self.assertEqual(l_xml.find('ConnectionName').text, TESTING_PANDORA_CONNECTION_DEVICE_NAME_0_0)
        self.assertEqual(l_xml.find('InputName').text, TESTING_PANDORA_CONNECTION_INPUT_NAME_0_0)
        self.assertEqual(l_xml.find('InputCode').text, TESTING_PANDORA_CONNECTION_INPUT_CODE_0_0)
        self.assertEqual(l_xml.find('Volume').text, TESTING_PANDORA_CONNECTION_DEFAULT_VOLUME_0_0)

    def test_03_AllDevices(self):
        """ Write the entire PandoraSection XML
        """
        l_xml = pandoraXml.write_pandora_section_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'D1-03-A - All Devices'))
        self.assertEqual(l_xml.attrib['Active'], TESTING_PANDORA_ACTIVE)
        self.assertEqual(l_xml.find('Type').text, TESTING_PANDORA_DEVICE_TYPE_0)


class E1_API(SetupMixin, unittest.TestCase):
    """ Test that we are initializing properly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)

    def test_01_Init(self):
        """ Test that the data structure is correct.
        """
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION], 'E1-01-D - Section', 180))
        l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        self.assertIsNone(l_base._API)
        self.assertEqual(l_base.Active, False)
        self.assertEqual(l_base.DeviceCount, 0)


class E2_API(SetupMixin, unittest.TestCase):
    """ Test that we write XML correctly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()

        # self.m_xml_pandora = self.m_xml.entertainment_sect.find('PandoraSection').find('Device')
        # self.m_pandora = pandoraXml.read_pandora_section_xml(self.m_pyhouse_obj)

    def test_02_Load(self):
        """ Test that the data structure is correct.
        """
        self.m_api.LoadXml(self.m_pyhouse_obj)
        l_pandora_sect = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        # print(PrettyFormatAny.form(l_pandora_sect, 'E2-02-A - Section', 180))
        # print(PrettyFormatAny.form(l_pandora_sect.Devices[0], 'E2-02-A - Section', 180))
        l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        self.assertEqual(l_base.Active, True)
        self.assertEqual(l_base.DeviceCount, 1)


class E3_API(SetupMixin, unittest.TestCase):
    """ Test that we write XML correctly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        self.m_api.LoadXml(self.m_pyhouse_obj)

    def test_03_Start(self):
        """ Test that the data structure is correct.
        """
        l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]

    def test_04_Save(self):
        """ Test that the data structure is correct.
        """
        l_xml = ET.Element('EntertainmentSection')
        l_section = self.m_api.SaveXml(l_xml)
        # print(PrettyFormatAny.form(l_section, 'E3-04-A - Section'))

    def test_05_Stop(self):
        """ Test that the data structure is correct.
        """
        l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]


class F1_Mqtt(SetupMixin, unittest.TestCase):
    """ Test that we handle messages properly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        self.m_api.LoadXml(self.m_pyhouse_obj)
        self.m_mqtt = MqttActions(self.m_pyhouse_obj)

    def test_01_Decode(self):
        """ Test that the data structure is correct.
        """
        l_topic = ['control']
        l_message = 'X'
        # l_log = self.m_api.decode(l_topic, CTL)
        # print(l_log)

    def test_02_Control(self):
        """ Test that the data structure is correct.
        """
        l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]


class F2_Extract(SetupMixin, unittest.TestCase):
    """ Test that we handle messages properly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        self.m_api.LoadXml(self.m_pyhouse_obj)

    def test_01_Time(self):
        """ Test that the data structure is correct.
        """
        l_obj = PandoraStatusData()
        l_res = PianoBarProcessControl(self.m_pyhouse_obj)._extract_playtime(l_obj, TIME_LN)
        # print(PrettyFormatAny.form(l_obj, 'F2-01-A - Status', 180))
        self.assertEqual(l_res.PlayingTime, '03:00')

    def test_02_Line(self):
        """ Test that the data structure is correct.
        """
        l_obj = PandoraStatusData()
        l_res = PianoBarProcessControl(self.m_pyhouse_obj)._extract_nowplaying(l_obj, PLAY_LN)
        # print(PrettyFormatAny.form(l_obj, 'F2-02-A - Status', 180))
        self.assertEqual(l_res.Album, 'Greatest Hits')
        self.assertEqual(l_res.Artist, 'Dave Koz')
        self.assertEqual(l_res.Likability, '3')
        self.assertEqual(l_res.Song, 'Love Is On The Way')
        self.assertEqual(l_res.Station, 'Smooth Jazz Radio')


class G1_Extract(SetupMixin, unittest.TestCase):
    """ Test that we handle messages properly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        self.m_api.LoadXml(self.m_pyhouse_obj)


class G2_Extract(SetupMixin, unittest.TestCase):
    """ Test that we handle messages properly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        self.m_api.LoadXml(self.m_pyhouse_obj)

# ## END DBK
