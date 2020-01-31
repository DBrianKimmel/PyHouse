"""
@name:      Modules/House/Entertainment/Pandora/_test/test_pandora.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 22, 2014
@summary:   Test

Passed all 17 tests - DBK - 2020-01-30
"""

__updated__ = '2020-01-30'

# Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

# Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Entertainment import EntertainmentPluginInformation
from Modules.House.Entertainment.Pandora import PandoraServiceInformation, PandoraServiceStatus
from Modules.House.Entertainment.Pandora.pandora import Api as pandoraApi, \
    ExtractPianobar, \
    PianobarProtocol, \
    LocalConfig as pandoraConfig

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

CTL = {
    'Sender' : 'Computer_1',
    'Control': 'PowerOff'
    }

TIME_LN = b'#   -03:00/03:10\r'
PLAY_LN = b'   "Love Is On The Way" by "Dave Koz" on "Greatest Hits" <3 @ Smooth Jazz Radio'

TEST_YAML = """\
Pandora:
    Name: Pandora service
    Comment: The Pandora music service
    Services:
        - Name: Primary
          Comment: main connection
          MaxSessions: 1
          Host:
              Name: pandora-pp
              Port: 1234
          Connection:
              Type: wire
              Family: Pioneer
              Model: VSX-833-K
              Input: CD
          Access:
              Name: d.briankimmel@gmail.com
              Password: !Secret1 encripted
"""

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
        l_yaml = YAML()
        self.m_test_config = l_yaml.load(TEST_YAML)
        self.m_config = pandoraConfig(self.m_pyhouse_obj)


class A0(unittest.TestCase):
    """ Prints the _test ID
    """

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_pandora')


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = pandoraApi(self.m_pyhouse_obj)

    def test_01_Pyhouse(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        self.assertIsNotNone(self.m_pyhouse_obj)

    def test_02_House(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A1-02-A - House'))
        self.assertIsNotNone(self.m_pyhouse_obj.House)

    def test_03_Entertainment(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'A1-03-A - Entertainment'))
        self.assertIsNotNone(self.m_pyhouse_obj.House.Entertainment)

    def test_04_Pandora(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment['Pandora'], 'A1-04-A - Pandora'))
        self.assertIsNotNone(self.m_pyhouse_obj.House.Entertainment['Pandora'])


class C1_Read(SetupMixin, unittest.TestCase):
    """ Check config loading
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Service0(self):
        """
        """
        l_config = self.m_test_config['Pandora']['Services'][0]
        # print('C1-01-A - {}'.format(l_config))
        # print(PrettyFormatAny.form(l_config, 'C1-01-B - PyHouse'))
        l_obj = self.m_config._extract_one_service(l_config)
        # print(PrettyFormatAny.form(l_obj, 'C1-01-C - Service 0'))
        self.assertEqual(l_obj.Name, 'Primary')
        self.assertEqual(l_obj.Comment, 'main connection')

    def test_03_Services(self):
        """
        """
        l_config = self.m_test_config['Pandora']['Services']
        print('C1-03-A - {}'.format(l_config))
        print(PrettyFormatAny.form(l_config, 'C1-03-B - PyHouse'))
        l_obj = self.m_config._extract_all_services(l_config)
        print(PrettyFormatAny.form(l_obj, 'C1-03-C - Services'))
        self.assertEqual(len(l_obj), 1)

    def test_04_Pandora(self):
        """
        """
        l_config = self.m_test_config['Pandora']
        # print('C1-04-A - {}'.format(l_config))
        # print(PrettyFormatAny.form(l_config, 'C1-04-B - PyHouse'))
        l_obj = self.m_config._extract_all_pandora(l_config)
        # print(PrettyFormatAny.form(l_obj, 'C1-04-C - PyHouse'))
        self.assertEqual(l_obj.Name, 'Pandora service')
        self.assertEqual(l_obj.Comment, 'The Pandora music service')
        self.assertEqual(len(l_obj.Services), 1)


class D1_PianoBarRxed(SetupMixin, unittest.TestCase):
    """ Test Getting data from piano bar
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Like(self):
        """ Test that the data structure is correct.
        """
        l_line = PLAY_LN
        l_like, _x = ExtractPianobar(self.m_pyhouse_obj)._extract_like(l_line)
        # print(l_like)
        self.assertEqual(l_like, '3')

    def test_02_Station(self):
        """ Test that the data structure is correct.
        """
        l_line = PLAY_LN
        l_like, _x = ExtractPianobar(self.m_pyhouse_obj)._extract_station(l_line)
        # print(l_like)
        self.assertEqual(l_like, 'Smooth Jazz Radio')


class D2_PianoBarRxed(SetupMixin, unittest.TestCase):
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


class E1_Api(SetupMixin, unittest.TestCase):
    """ Test that we are initializing properly
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = pandoraApi(self.m_pyhouse_obj)

    def test_01_Init(self):
        """ Test that the data structure is correct.
        """
        self.m_pyhouse_obj.House.Entertainment['Pandora'] = EntertainmentPluginInformation()
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment['Pandora'], 'E1-01-D - Section', 180))
        l_base = self.m_pyhouse_obj.House.Entertainment['Pandora']
        self.assertIsNone(l_base._Api)
        self.assertEqual(l_base.ServiceCount, 0)


class F2_Extract(SetupMixin, unittest.TestCase):
    """ Test that we handle messages properly
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = pandoraApi(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment['Pandora'] = EntertainmentPluginInformation()

    def test_01_Time(self):
        """ Test that the data structure is correct.
        """
        l_obj = PandoraServiceInformation()
        l_res = ExtractPianobar(self.m_pyhouse_obj)._extract_playtime(l_obj, TIME_LN)
        print(PrettyFormatAny.form(l_obj, 'F2-01-A - Status'))
        print(PrettyFormatAny.form(l_res, 'F2-01-B - Status'))
        self.assertEqual(l_res.TimeTotal, '03:10')
        self.assertEqual(l_res.TimeLeft, '03:00')

    def test_02_Line(self):
        """ Test that the data structure is correct.
        """
        l_obj = PandoraServiceStatus()
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
        self.m_api = pandoraApi(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment['Pandora'] = EntertainmentPluginInformation()


class G2_Extract(SetupMixin, unittest.TestCase):
    """ Test that we handle messages properly
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = pandoraApi(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment['Pandora'] = EntertainmentPluginInformation()


class Z9_End(SetupMixin, unittest.TestCase):
    """
    This section tests building commands to the onkyo device
    """

    def test_Done(self):
        """ Be sure that the XML contains the right stuff.
        """
        pass

# ## END DBK
