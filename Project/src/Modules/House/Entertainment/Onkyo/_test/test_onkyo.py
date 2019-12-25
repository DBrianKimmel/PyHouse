"""
@name:      PyHouse/src/Modules/Housing/Entertainment/_test/test_onkyo.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 22, 2014
@summary:   Test

Run 'PyHouse/src/_test/test_xml_data.py' if XML is corrupted.

Passed all 8 tests - DBK - 2018-11-03

"""

__updated__ = '2019-12-25'

# Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

# from twisted._test import proto_helpers
# from twisted.internet.protocol import ClientCreator

# Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.House.Entertainment.Onkyo.onkyo import LocalConfig as onkyoConfig

MSG_01 = """
{
    'Sender': 'pi-01-pp',
    'DateTime': '2019-05-03 23:27:13.713069',
    'Power': 'On',
    'Zone': '1'
}
"""

TEST_YAML = """\
Onkyo:
    Name: Onkyo components
    Comment: The Onkyo A/V device
    Device:
        - Name: Onkyo A/V Receiver
          Comment: Main Receiver
          Host:
              Name: onkyo-01-pp
              Port: 8102
          Type: Receiver
          Model: TX-555
"""

TEST_YAML_DEV = """\
UnitType: 1
ControlCommands:
    Power:
        - PWR
        - PWZ
    Volume:
        - MVL
        - ZVL
    Mute:
        - AMT
        - ZMT
    InputSelection:
        - SLI
        - SLZ
Arguments:
    Power:
        'Off': '00'
        'On': '01'
        '?': 'QSTN'
    Volume:
        'Up': 'UP'
        'Down': 'DOWN'
        '?': 'QSTN'
InputSelection:
    'Video1': '00'
    'Cbl/Sat': '01'       # 'VIDEO2', 'CBL/SAT'
    'Game': '02'          # 'VIDEO3', 'GAME/TV', 'GAME', 'GAME1'
    'Aux': '03'           # 'VIDEO4', 'AUX1(AUX)'
    'Pc': '05'            # 'VIDEO6', 'PC'
    'Bd/Dvd': '10'        # 'DVD', 'BD/DVD'
    'Strmbox': '11'       # 'STRM BOX'
    'TV': '12'            # 'TV'
    'Phono': '22'         # 'PHONO'
    'Cd': '23'            # 'CD', 'TV/CD'
    'Fm': '24'            # FM + PRS 00 + TUN 10330 + PR3 00 + TU3 10330
    'Am': '25'            # AM + PRS 00 + TUN 00830 + PR3 00 + TU3 00830
    'BlueTooth': '2E'
    'Network': '2B'
Zones:
    0: Main
    1: Lanai
"""


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_pyhouse_obj.House.Entertainment['onkyo'] = {}
        l_yaml = YAML()
        self.m_test_config = l_yaml.load(TEST_YAML)


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_x', 'title')  # so it is defined when printing is cleaned up.
        print('Id: test_onkyo')


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Objects(self):
        """ Be sure that the XML contains the right stuff.
        """


class B1_Data(SetupMixin, unittest.TestCase):
    """
    Test that the Onkyo XML is correct.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_00_setup(self):
        """
        """
        l_onkyo = onkyoConfig(self.m_pyhouse_obj)._extract_all_onkyo(self.m_test_config, self)
        print(PrettyFormatAny.form(l_onkyo, 'B1-00-A - Onkyo'))

    def test_01_Onkyo(self):
        l_yaml = YAML()
        l_dev = l_yaml.load(TEST_YAML_DEV)
        print(PrettyFormatAny.form(l_dev, 'B1-01-A - PyHouse'))
        print(PrettyFormatAny.form(l_dev['ControlCommands'], 'B1-01-B - Commands'))
        print(PrettyFormatAny.form(l_dev['Arguments'], 'B1-01-C - Arguments'))
        print(PrettyFormatAny.form(l_dev['InputSelect'], 'B1-01-D - Inputs'))
        print(PrettyFormatAny.form(l_dev['Zones'], 'B1-01-E - Zones'))

    def test_02_Device0(self):
        l_obj = self.m_pyhouse_obj.House.Entertainment['onkyo'].Devices[0]
        # print(PrettyFormatAny.form(l_obj, 'B1-02-A - PyHouse', 190))

    def test_03_Device1(self):
        l_obj = self.m_pyhouse_obj.House.Entertainment['onkyo'].Devices[1]
        # print(PrettyFormatAny.form(l_obj, 'B1-03-A - PyHouse', 190))


class C1_Yaml(SetupMixin, unittest.TestCase):
    """
    This section tests the reading of the YAML file for each of the Onkyo devices.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_00_Yaml(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_yaml, 'B3-01-A - Yaml', 190))
        self.assertGreater(len(self.m_yaml), 4)

    def test_01_Unit(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print('B3-01-A - Unit type: {}'.format(self.m_yaml['UnitType']))
        self.assertEqual(self.m_yaml['UnitType'], 1)

    def test_02_Cmds(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_yaml['ControlCommands'], 'B3-02-A - Yaml'))
        self.assertEqual(self.m_yaml['ControlCommands']['Power'][0], 'PWR')
        self.assertEqual(self.m_yaml['ControlCommands']['Power'][1], 'PWZ')
        self.assertEqual(self.m_yaml['ControlCommands']['Volume'][0], 'MVL')
        self.assertEqual(self.m_yaml['ControlCommands']['Volume'][1], 'ZVL')
        self.assertEqual(self.m_yaml['ControlCommands']['Mute'][0], 'AMT')
        self.assertEqual(self.m_yaml['ControlCommands']['Mute'][1], 'ZMT')
        self.assertEqual(self.m_yaml['ControlCommands']['InputSelect'][0], 'SLI')
        self.assertEqual(self.m_yaml['ControlCommands']['InputSelect'][1], 'SLZ')

    def test_03_Args(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_yaml['Arguments'], 'B3-03-A - Yaml', 190))
        # print(PrettyFormatAny.form(self.m_yaml['Arguments']['Power'], 'B3-03-B - Yaml', 190))
        self.assertEqual(self.m_yaml['Arguments']['Power']['Off'], '00')
        self.assertEqual(self.m_yaml['Arguments']['Power']['On'], '01')
        self.assertEqual(self.m_yaml['Arguments']['Power']['?'], 'QSTN')

    def test_04_Input(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_yaml['InputSelect'], 'B3-04-A - Yaml', 190))
        self.assertEqual(self.m_yaml['InputSelect']['Cbl/Sat'], '01')
        self.assertEqual(self.m_yaml['InputSelect']['Game'], '02')
        self.assertEqual(self.m_yaml['InputSelect']['Aux'], '03')


class C3_Command(SetupMixin, unittest.TestCase):
    """
    This section tests building commands to the onkyo device
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Zone1(self):
        """ Be sure that the XML contains the right stuff.
        """

    def test_02_Zone2(self):
        """ Be sure that the XML contains the right stuff.
        """

    def test_03_VolZ1(self):
        """ Be sure that the XML contains the right stuff.
        """

    def test_04_VolZ2(self):
        """ Be sure that the XML contains the right stuff.
        """


class D1_Protocol(SetupMixin, unittest.TestCase):
    """
    This section tests
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_reactor = self.m_pyhouse_obj._Twisted.Reactor

    def tearDown(self):
        if self.m_client is not None:
            self.m_client.transport.looseConnection()
        return self.m_port.stopListening()
        pass

    def _test(self, p_operation, a, b, p_expected):
        self.proto.dataReceived('%s %d %d\r\n' % (p_operation, a, b))
        self.assertEqual(int(self.tr.value()), p_expected)

    def test_01_Factory(self):
        """ Be sure that the XML contains the right stuff.
        """

    def test_02_Protocol(self):
        """ Be sure that the XML contains the right stuff.
        """

    def test_03_Transport(self):
        """ Be sure that the XML contains the right stuff.
        """

    def test_04_Connection(self):
        """ Be sure that the XML contains the right stuff.
        """


class E1_Data(SetupMixin, unittest.TestCase):
    """
    Test that the Onkyo XML is correct.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_00_setup(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'E1-00-A - PyHouse'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'E1-00-B - House'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'E1-00-C - Entertainment'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins, 'E1-00-D - Plugins'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'], 'E1-00-E - Onkyo'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'].Devices, 'E1-00-F - Devices'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'].Devices[0], 'E1-00-G - Devices'))
        self.assertEqual(self.m_pyhouse_obj.House.Entertainment.PluginCount, 5)

    def test_01_Onkyo(self):
        l_obj = self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo']
        print(PrettyFormatAny.form(l_obj, 'E1-01-A - PyHouse', 190))
        self.assertEqual(l_obj.DeviceCount, 2)
        self.assertEqual(l_obj.Name, 'onkyo')

    def test_02_Device0(self):
        l_obj = self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'].Devices[0]
        print(PrettyFormatAny.form(l_obj, 'E1-01-A - PyHouse', 190))

    def test_03_Device1(self):
        l_obj = self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'].Devices[1]
        print(PrettyFormatAny.form(l_obj, 'E1-01-A - PyHouse', 190))


class E2_Message(SetupMixin, unittest.TestCase):
    """
    This section tests
    """

    def setUp(self):
        SetupMixin.setUp(self)
        # l_ret = entertainmentXML().read_entertainment_all(self.m_pyhouse_obj)
        # self.m_reactor = self.m_pyhouse_obj._Twisted.Reactor

    def test_01_Zone(self):
        """ Be sure that the XML contains the right stuff.
        """


class F3_Yaml(SetupMixin, unittest.TestCase):
    """
    This section tests building commands to the onkyo device
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Power(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_queue, 'F3-01-A - ZoneQueue', 190))

    def test_02_Vol(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.m_queue.Command = 'Volume'
        self.m_queue.Args = 27
        # print(PrettyFormatAny.form(self.m_queue, 'F3-01-A - ZoneQueue', 190))

# ## END DBK
