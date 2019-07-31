"""
@name:      Modules/Housing/test/test_house.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 8, 2013
@summary:   Test handling the information for a house.

Passed all 16 tests - DBK - 2019-05-11

"""

__updated__ = '2019-07-28'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import HouseInformation, PyHouseInformation
from Modules.Housing.house import \
    API as houseAPI, \
    Config as houseConfig, \
    Utility as houseUtil
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_house')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local
        module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly.
        """
        print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A1-01-B - House'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Rooms, 'A1-01-C - Rooms'))
        self.assertIsInstance(self.m_pyhouse_obj, PyHouseInformation)
        self.assertIsInstance(self.m_pyhouse_obj.House, HouseInformation)


class C1_Read(SetupMixin, unittest.TestCase):
    """
    This section tests the reading of the config used by house.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Load(self):
        """
        """
        l_node = houseConfig(self.m_pyhouse_obj).LoadYamlConfig()
        print('C1-01-A - Load: {}'.format(l_node.Yaml))

    def test_09_API(self):
        houseUtil._init_component_apis(self.m_pyhouse_obj, self)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'B1-1-A - XML'))
        self.assertEqual(self.m_pyhouse_obj._Uuids.All, {})


class C2_Write(SetupMixin, unittest.TestCase):
    """
    This section tests the writing of XML used by house.
    """

    def setUp(self):
        SetupMixin.setUp(self)


class P1_API(SetupMixin, unittest.TestCase):
    """ Test the major API functions
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = houseAPI(self.m_pyhouse_obj)

    def test_01_Init(self):
        """ Create a JSON object for Location.
        """
        # print(PrettyFormatAny.form(self.m_api, 'P1-01-A - API'))
        pass

    def test_02_Load(self):
        _l_configl = self.m_api.LoadConfig(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'P1-02-A - API'))

    def test_03_Start(self):
        pass

    def test_04_SaveXml(self):
        self.m_api.LoadConfig(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'P1-04-A - House'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj._Families, 'P1-04-B - House'))
        # print(PrettyFormatAny.form(l_xml, 'P1-04-D - API'))

# ## END DBK
