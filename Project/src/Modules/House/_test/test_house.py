"""
@name:      Modules/House/_test/test_house.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 8, 2013
@summary:   Test handling the information for a house.

Passed all 11 tests - DBK - 2020-01-27

"""
from Modules.House import HouseInformation

__updated__ = '2020-02-02'

# Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.house import Api as houseApi
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

TEST_YAML = """\
House:
   Name: PinkPoppy
   Modules:  # Uncomment to use module.
      - Family
      - Entertainment
      # - HVAC
      # - Irrigation
      - Lighting
      # - Pool
      # - Rules
      - Scheduling
      # - Security
      # - Sync
"""


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        l_yaml = YAML()
        self.m_test_config = l_yaml.load(TEST_YAML)


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_house')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local
        module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_PyHouse(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        self.assertIsNotNone(self.m_pyhouse_obj)

    def test_02_House(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A1-02-A - House'))
        self.assertIsNotNone(self.m_pyhouse_obj.House)
        self.assertIsInstance(self.m_pyhouse_obj.House, HouseInformation)

    def test_03_Location(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Location, 'A1-03-A - Location'))
        self.assertIsNotNone(self.m_pyhouse_obj.House.Location)


class C1_Read(SetupMixin, unittest.TestCase):
    """
    This section tests the reading of the config used by house.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Load(self):
        """
        """


class C2_Write(SetupMixin, unittest.TestCase):
    """
    This section tests the writing of XML used by house.
    """

    def setUp(self):
        SetupMixin.setUp(self)


class P1_Api(SetupMixin, unittest.TestCase):
    """ Test the major Api functions
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = houseApi(self.m_pyhouse_obj)

    def test_01_Init(self):
        """ Create a JSON object for Location.
        """
        # print(PrettyFormatAny.form(self.m_api, 'P1-01-A - Api'))
        pass

    def test_02_Load(self):
        """
        """
        # print(PrettyFormatAny.form(l_xml, 'P1-02-A - Api'))

    def test_03_Start(self):
        pass

    def test_04_SaveXml(self):
        """
        """
        # self.m_api.LoadConfig()
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'P1-04-A - House'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj._Families, 'P1-04-B - House'))
        # print(PrettyFormatAny.form(l_xml, 'P1-04-D - Api'))

# ## END DBK
