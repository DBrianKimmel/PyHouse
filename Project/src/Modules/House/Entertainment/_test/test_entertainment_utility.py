"""
@name:      Modules/House/Entertainment/_test/test_entertainment_utility.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 25, 2019
@summary:   Test

Passed all 13 tests - DBK - 2019-12-25

"""

__updated__ = '2019-12-25'

# Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML
import json

# Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Entertainment import entertainment_utility as E_U
from Modules.Core.Utilities import json_tools
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

TEST_YAML = """\
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
        l_yaml = YAML()
        self.m_yaml = l_yaml.load(TEST_YAML)


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'so PrettyFormatAny is defined')
        print('Id: test_entertainment_utility')


class C1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_1_BuildObjects(self):
        """
        """
        # print('C1-01-A - Unit type: {}'.format(self.m_yaml))
        l_dict = E_U.extract_device_config_file(self.m_yaml)
        # print(PrettyFormatAny.form(l_dict, 'C1-01-B - Dict'))
        l_json = json.dumps(l_dict, indent=4)
        print('C1-01-C - JSON: {}'.format(l_json))

# ## END DBK
