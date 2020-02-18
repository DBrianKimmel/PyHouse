"""
@name:      Modules/House/Security/_test/test_motion_detectors.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 29, 2019
@summary:   Test

Passed all 13 tests - DBK - 2018-02-13

"""

__updated__ = '2019-12-29'

# Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Security.motion_detectors import Api as motionApi
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

TEST_YAML = """\
Motion_Detectors:
   - Name: MotionLiving
     Comment: Living Room
     Family:
        Name: Insteon
        Address: 31.75.85
"""


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        l_yaml = YAML()
        self.m_test_config = l_yaml.load(TEST_YAML)
        self.m_motionApi = motionApi(self.m_pyhouse_obj)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_motion_detectors')


class C1_ConfigRead(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Detector(self):
        """ Test reading the device portion of the config.
        """
        # print('C1-01')
        l_yaml = self.m_test_config['Motion_Detectors'][0]
        # print('C1-01-A - Yaml: ', l_yaml)
        l_ret = self.m_motionApi.m_local_config._extract_one_motion_sensor(l_yaml)
        # print(PrettyFormatAny.form(l_ret, 'C1-01-B - Motion_Detector'))
        self.assertEqual(l_ret.Name, 'MotionLiving')
        self.assertEqual(l_ret.Comment, 'Living Room')
        self.assertEqual(l_ret.DeviceType, 'Security')
        self.assertEqual(l_ret.DeviceSubType, 'MotionDetector')
        self.assertEqual(l_ret.Family.Name, 'insteon')
        self.assertEqual(l_ret.Family.Address, '31.75.85')

    def test_03_Detectors(self):
        """ Test reading of the Lights config file.
        """
        l_yaml = self.m_test_config['Motion_Detectors']
        # print(PrettyFormatAny.form(l_yaml, 'C1-03-A - Yaml'))
        l_ret = self.m_motionApi.m_local_config._extract_all_motion_sensors(l_yaml)
        # print(PrettyFormatAny.form(l_ret, 'C1-03-B - Node'))
        self.assertEqual(len(l_ret), 1)
        self.assertEqual(l_ret[0].Name, 'MotionLiving')

# ## END DBK
