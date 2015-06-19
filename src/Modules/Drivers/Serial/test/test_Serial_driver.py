"""
@name:      PyHouse/src/Modules/Drivers/Serial/test/test_Serial_driver.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013_2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on May 4, 2013
@summary:   This module is for testing local node data.

Passed 5 API tests - DBK - 2014-07-27
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ControllerData
from Modules.Drivers.Serial import Serial_driver
from Modules.Families import family
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A01_API(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_api = Serial_driver.API()
        self.m_controller_obj = self._fake_params()
        self.m_controller_obj.BaudRate = 19200

    def _fake_params(self):
        l_obj = ControllerData()
        l_obj.BaudRate = 19200
        return l_obj

    def test_01_Init(self):
        pass

    def test_02_Start(self):
        self._fake_params()
        self.m_api.Start(self.m_pyhouse_obj, self.m_controller_obj)
        PrettyPrintAny(self.m_controller_obj, 'Controller Obj', 120)

    def test_03_Stop(self):
        self.m_api.Start(self.m_pyhouse_obj, self.m_controller_obj)
        self.m_api.Stop()

    def test_04_Read(self):
        self.m_api.Start(self.m_pyhouse_obj, self.m_controller_obj)
        self.m_api.Read()

    def test_05_Write(self):
        self.m_api.Start(self.m_pyhouse_obj, self.m_controller_obj)
        self.m_api.Write('xxx')

# ## END
