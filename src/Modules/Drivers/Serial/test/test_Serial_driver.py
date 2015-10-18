"""
@name:      PyHouse/src/Modules/Drivers/Serial/test/test_Serial_driver.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013_2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on May 4, 2013
@summary:   This module is for testing local node data.

Passed all 1 tests - DBK - 2015-07-30
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ControllerData
from Modules.Drivers.Serial import Serial_driver
from Modules.Families.family import API as familyAPI
from Modules.Lighting.lighting import API as lightingAPI
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_pyhouse_obj.House.FamilyData = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        lightingAPI(self.m_pyhouse_obj).LoadXml(self.m_pyhouse_obj)


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def _fake_params(self):
        l_obj = ControllerData()
        l_obj.BaudRate = 19200
        return l_obj

    def test_01_Controllers(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Controllers, 'PyHouse Controllers'))
        self.assertEqual(len(self.m_pyhouse_obj.House.Controllers), 2)


class B1_API(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Start(self):
        pass

# ## END
