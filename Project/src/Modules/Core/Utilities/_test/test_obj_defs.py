"""
@name:      C:/Users/briank/workspace/PyHouse/src/Modules.Core.Utilities._test/test_obj_defs.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 7, 2015
@Summary:

Passed all 3 tests - DBK - 2016-11-22

"""

__updated__ = '2016-11-22'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Core.Utilities.obj_defs import GetPyhouse
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_obj_defs')


class D1_GetPyHouse(SetupMixin, unittest.TestCase):
    """Test GetPyhouse class functionality
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_House(self):
        l_pyh = GetPyhouse(self.m_pyhouse_obj).House()
        # self.assertEqual(l_pyh.Name, 'Test House')
        # self.assertEqual(l_pyh.Key, 0)
        # self.assertEqual(l_pyh.Active, True)

    def test_01_Schedules(self):
        l_pyh = GetPyhouse(self.m_pyhouse_obj).Schedules()
        # self.assertEqual(l_pyh.Schedules, {})
        pass

# ## END DBK
