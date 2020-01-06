"""
@name:      Modules/House/Family/Hue/_test/test_Hue_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 18, 2017
@summary:   Test

Passed all 2 tests - DBK - 2018-01-27

"""
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

__updated__ = '2019-10-16'

# Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Family.hue import hue_device
from Modules.House.Family.hue.hue_device import HueInformation

TEST_YAML = """\
Hue:
    - Name: HueHub
      Comment: For philips hue lights
      Family:
          Name: Hue
      Host:
          Name: hue-node
          Port: None
      Access:
          Apikey: 9nR8rI12345678OabMWu12345678jBS2EWHoFYy3
          Password: !secret EncriptedPassword1

"""


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        l_yaml = YAML()
        self.m_test_config = l_yaml.load(TEST_YAML)
        self.m_local_config = hue_device.LocalConfig(self.m_pyhouse_obj)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_Hue_device')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Build(self):
        """ The basic read info as set up
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A1-01-B - House'))
        self.assertIsInstance(self.m_pyhouse_obj.House.Family, dict)


class C01_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = hue_device.Api(self.m_pyhouse_obj)
        self.m_device = HueInformation()

    def test_01_Init(self):
        """ Be sure that the XML contains the right stuff.
        """
        pass


def suite():
    suite = unittest.TestSuite()
    # suite.addTest(Test_02_Api('test_0202_Init'))
    return suite

# ## END DBK
