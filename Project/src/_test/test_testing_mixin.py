"""
@name:      PyHouse/Projectsrc/_test/test_testing_mixin.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Oct 6, 2014
@Summary:

Passed all 16 tests - DBK - 2019-06-23

"""

__updated__ = '2019-06-23'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG, XML_EMPTY
from test.testing_mixin import SetupPyHouseObj, TEST_PATH
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.data_objects import PyHouseInformation, ComputerInformation, HouseInformation


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)

    def setUpObj(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)

    def setUpXml(self, p_root):
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)

    def setUpYaml(self, p_root):
        self.m_yaml = SetupPyHouseObj().BuildYaml(p_root)


class A0(unittest.TestCase):

    def test_00_Print(self):
        print('Id: test_testing_mixin')


class A1_Setup(SetupMixin, unittest.TestCase):
    """ This section tests the SetupMixin Class
    """

    def setUp(self):
        pass

    def test_01_BuildObjs(self):
        """ Be sure that the PyHouse obj is built correctly
        """
        l_root = None
        l_obj = SetupPyHouseObj().BuildPyHouseObj(l_root)
        print(PrettyFormatAny.form(l_obj, 'A1-02-A - PyHouseObj', 90))
        self.assertIsInstance(l_obj, PyHouseInformation)
        self.assertIsInstance(l_obj.Computer, ComputerInformation)
        self.assertIsInstance(l_obj.House, HouseInformation)

    def test_02_XML(self):
        """ Be sure that the XML contains the right stuff.
        """
        pass

    def test_03_YAML(self):
        """ Be sure that the YAML contains the right stuff.
        """
        l_root = None
        l_obj = SetupPyHouseObj().BuildPyHouseObj(l_root)
        # print(PrettyFormatAny.form(l_obj, 'A1-03-A - PyHouseObj', 90))
        print(PrettyFormatAny.form(l_obj._Config, 'A1-03-B - _Config', 90))


class B1_Empty(SetupMixin, unittest.TestCase):
    """ This section tests the SetupMixin Class
    """

    def setUp(self):
        SetupMixin.setUpObj(self, ET.fromstring(XML_EMPTY))
        pass

    def test_01_Obj(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'B1-01-A - PyHouse'))
        pass

    def test_02_Computer(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'B1-02-A - PyHouse.Computer'))
        pass

    def test_03_House(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'B1-03-A - PyHouse.House'))
        pass

    def test_04_Location(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Location, 'B1-04-A - PyHouse.House.Location'))
        pass


class B2_Long(SetupMixin, unittest.TestCase):
    """ This section tests the SetupMixin Class
    """

    def setUp(self):
        SetupMixin.setUpObj(self, ET.fromstring(XML_LONG))
        pass

    def test_01_Obj(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'B2-01-A - PyHouse'))
        pass

    def test_02_Computer(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'B2-02-A - PyHouse.Computer'))
        pass

    def test_03_House(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'B2-03-A - PyHouse.House'))
        pass

    def test_04_Location(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Location, 'B2-04-A - PyHouse.House.Location'))
        pass


class C1_Build(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by inernet.
    """

    def setUp(self):
        self.m_api = SetupPyHouseObj()

    def test_01_Computer(self):
        l_pyhouse = self.m_pyhouse_obj
        l_config = self.m_api._build_computer(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_config, 'C1-01-A - Config'))
        # self.assertDictEqual(l_config.Email, {})
        # self.assertDictEqual(l_config.InternetConnection, {})
        # self.assertDictEqual(l_config.Nodes, {})
        # self.assertDictEqual(l_config.Web, {})
        pass

    def test_02_House(self):
        l_obj = {}
        l_config = self.m_api._build_house(l_obj)
        # print(PrettyFormatAny.form(l_config, 'C1-02-A - Config'))
        self.assertEqual(l_config.Key, 0)

    def test_03_PyHouse(self):
        l_root = None
        l_config = self.m_api.BuildPyHouseObj(l_root)
        # #print(PrettyFormatAny.form(l_root, 'C1-04-A - Root'))
        pass

    def test_05_XML(self):
        l_root = ET.fromstring(XML_LONG)
        l_config = self.m_api.BuildXml(l_root)
        # print(PrettyFormatAny.form(l_config, 'C1-05-A - Config'))
        pass

# ## END DBK
