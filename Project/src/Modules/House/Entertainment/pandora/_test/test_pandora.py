"""
@name:      Modules/House/Entertainment/pandora/_test/test_pandora.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 22, 2014
@summary:   Test

Passed all 17 tests - DBK - 2019-08-30
"""

__updated__ = '2019-08-30'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Entertainment.entertainment import API as entertainmentAPI
from Modules.House.Entertainment.pandora.pandora import \
    API as pandoraAPI, \
    SECTION, \
    MqttActions, \
    PandoraServiceData, \
    PandoraServiceStatusData, \
    ExtractPianobar, \
    PianobarProtocol

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

CTL = {
    'Sender' : 'Computer_1',
    'Control': 'PowerOff'
    }

TIME_LN = b'#   -03:00/03:00\r'
PLAY_LN = b'   "Love Is On The Way" by "Dave Koz" on "Greatest Hits" <3 @ Smooth Jazz Radio'

BUFFER_01 = \
b'Welcome to pianobar (2016.06.02)! Press ? for a list of commands.\r\n' \
b'(i) Login... \r\n' \
b'Ok.\r\n' \
b'(i) Get stations... \r\n' \
b'Ok.\r\n' \
b'|>  Station "QuickMix" (1608513919875785623)\r\n' \
b'  Station "QuickMix" (1608513919875785623)\r\n' \
b'(i) Receiving new playlist... \r\n' \
b'Ok.\r\n' \
b'|>  "Go For It" by "Bernie Williams" on "Moving Forward" @ Smooth Jazz Radio\r\n'  \
b'  "Go For It" by "Bernie Williams" on "Moving Forward" @ Smooth Jazz Radio\r\n'


class SetupMixin:

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_xml = SetupPyHouseObj().BuildXml()


class A0(unittest.TestCase):
    """ Prints the _test ID
    """

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_pandora')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up pyhouse_obj and the XML tags that we will need
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly.
        """
        # print(PrettyFormatAny.form(l_xml, 'A1-01-A - Entertainment XML'))


class B1_Xml(SetupMixin, unittest.TestCase):
    """ Test that we have read the xml in properly and that essential items have loaded into the pyhouse_obj properly.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Init(self):
        """ Test that the data structure is correct.
        """
        l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        # print(PrettyFormatAny.form(l_base, 'B1-01-A - Pandora', 180))
        self.assertEqual(l_base.ServiceCount, 1)
        self.assertEqual(l_base.DeviceCount, 0)

    def test_02_Service0(self):
        """ Test that the data structure is correct.
        """
        l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Services[0]
        # print(PrettyFormatAny.form(l_base, 'B1-02-A - Section', 180))


class C1_PianoBarRxed(SetupMixin, unittest.TestCase):
    """ Test that we have read the xml in properly and that essential items have loaded into the pyhouse_obj properly.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Like(self):
        """ Test that the data structure is correct.
        """
        l_line = PLAY_LN
        l_like, _l_rest = ExtractPianobar(self.m_pyhouse_obj)._extract_like(l_line)
        # print(l_like, l_rest)
        self.assertEqual(l_like, '3')

    def test_02_Station(self):
        """ Test that the data structure is correct.
        """
        l_line = PLAY_LN
        l_like, _l_rest = ExtractPianobar(self.m_pyhouse_obj)._extract_station(l_line)
        # print(l_like, l_rest)
        self.assertEqual(l_like, 'Smooth Jazz Radio')


class C2_PianoBarRxed(SetupMixin, unittest.TestCase):
    """ Test that we have read the xml in properly and that essential items have loaded into the pyhouse_obj properly.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Like(self):
        """ Test that the data structure is correct.
        """
        l_buffer = BUFFER_01
        # print(l_buffer)
        while l_buffer:
            l_buffer, l_line = PianobarProtocol(self.m_pyhouse_obj)._get_line(l_buffer)
            print(l_line)


class E1_API(SetupMixin, unittest.TestCase):
    """ Test that we are initializing properly
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)

    def test_01_Init(self):
        """ Test that the data structure is correct.
        """
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginInformation()
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION], 'E1-01-D - Section', 180))
        l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        self.assertIsNone(l_base._API)
        self.assertEqual(l_base.Active, False)
        self.assertEqual(l_base.ServiceCount, 0)


class E2_API(SetupMixin, unittest.TestCase):
    """ Test that we write XML correctly
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginInformation()

        # self.m_xml_pandora = self.m_xml.entertainment_sect.find('PandoraSection').find('Device')
        # self.m_pandora = pandoraXml.read_pandora_section_xml(self.m_pyhouse_obj)

    def test_02_Load(self):
        """ Test that the data structure is correct.
        """
        self.m_api.LoadXml(self.m_pyhouse_obj)
        _l_pandora_sect = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        # print(PrettyFormatAny.form(l_pandora_sect, 'E2-02-A - Section', 180))
        # print(PrettyFormatAny.form(l_pandora_sect.Services, 'E2-02-A - Section', 180))
        l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        # self.assertEqual(l_base.Active, True)
        self.assertEqual(l_base.ServiceCount, 1)


class E3_API(SetupMixin, unittest.TestCase):
    """ Test that we write XML correctly
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginInformation()
        self.m_api.LoadXml(self.m_pyhouse_obj)

    def test_03_Start(self):
        """ Test that the data structure is correct.
        """
        _l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]

    def test_04_Save(self):
        """ Test that the data structure is correct.
        """
        _l_section = self.m_api.SaveXml(l_xml)
        # print(PrettyFormatAny.form(l_section, 'E3-04-A - Section'))

    def test_05_Stop(self):
        """ Test that the data structure is correct.
        """
        _l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]


class F1_Mqtt(SetupMixin, unittest.TestCase):
    """ Test that we handle messages properly
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginInformation()
        self.m_api.LoadXml(self.m_pyhouse_obj)
        self.m_mqtt = MqttActions(self.m_pyhouse_obj)

    def test_01_Decode(self):
        """ Test that the data structure is correct.
        """
        _l_topic = ['control']
        _l_message = 'X'
        # l_log = self.m_api.decode(l_topic, CTL)
        # print(l_log)

    def test_02_Control(self):
        """ Test that the data structure is correct.
        """
        _l_base = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]


class F2_Extract(SetupMixin, unittest.TestCase):
    """ Test that we handle messages properly
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginInformation()
        self.m_api.LoadXml(self.m_pyhouse_obj)

    def test_01_Time(self):
        """ Test that the data structure is correct.
        """
        l_obj = PandoraServiceData()
        l_res = ExtractPianobar(self.m_pyhouse_obj)._extract_playtime(l_obj, TIME_LN)
        # print(PrettyFormatAny.form(l_obj, 'F2-01-A - Status', 180))
        self.assertEqual(l_res.PlayingTime, '03:00')

    def test_02_Line(self):
        """ Test that the data structure is correct.
        """
        l_obj = PandoraServiceStatusData()
        l_res = ExtractPianobar(self.m_pyhouse_obj)._extract_nowplaying(l_obj, PLAY_LN)
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
        SetupMixin.setUp(self)
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginInformation()
        self.m_api.LoadXml(self.m_pyhouse_obj)


class G2_Extract(SetupMixin, unittest.TestCase):
    """ Test that we handle messages properly
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_entAPI = entertainmentAPI(self.m_pyhouse_obj)
        self.m_api = pandoraAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginInformation()
        self.m_api.LoadXml(self.m_pyhouse_obj)

# ## END DBK