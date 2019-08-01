"""
@name:      PyHouse/Project/src/Modules/Drivers/Serial/_test/test_Serial_driver.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013_2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on May 4, 2013
@summary:   This module is for testing local node data.

Passed all 9 tests - DBK - 2019-01-10
"""

__updated__ = '2019-07-09'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ControllerInformation
from Modules.Drivers.Serial import Serial_driver
from Modules.Families.family import API as familyAPI
from Modules.Housing.Lighting.lighting import API as lightingAPI
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_pyhouse_obj._Families = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        #
        lightingAPI(self.m_pyhouse_obj).LoadXml(self.m_pyhouse_obj)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_Serial_driver')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def _fake_params(self):
        l_obj = ControllerInformation()
        l_obj.BaudRate = 19200
        return l_obj

    def test_01_PyHouse(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        self.assertEqual(len(self.m_pyhouse_obj.House.Lighting.Controllers), 2)

    def test_02_House(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'House'))
        self.assertEqual(len(self.m_pyhouse_obj.House.Lighting.Controllers), 2)

    def test_03_Controllers(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting.Controllers, 'PyHouse Controllers'))
        self.assertEqual(len(self.m_pyhouse_obj.House.Lighting.Controllers), 2)

    def test_04_Twisted(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj._Twisted, 'Twisted'))
        self.assertEqual(len(self.m_pyhouse_obj.House.Lighting.Controllers), 2)


class A2_Setup(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_FindPort(self):
        pass


class B1_Serial(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = Serial_driver.API(self.m_pyhouse_obj.House)

    def test_01_Open(self):
        l_controller = self.m_pyhouse_obj.House.Lighting.Controllers[0]
        l_ret = self.m_api.open_serial_driver(self.m_pyhouse_obj, l_controller)
        # print(PrettyFormatAny.form(l_ret, 'B1-01-A - open'))


class B2_API(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Start(self):
        pass


class B3_API(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Start(self):
        pass

# ## END
