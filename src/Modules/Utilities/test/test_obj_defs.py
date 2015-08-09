"""
@name:      C:/Users/briank/workspace/PyHouse/src/Modules/Utilities/test/test_obj_defs.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 7, 2015
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Utilities.obj_defs import GetPyhouse
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_version = '1.4.0'


class D1_GetPyHouse(SetupMixin, unittest.TestCase):
    """Test GetPyhouse class functionality
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_House(self):
        l_pyh = GetPyhouse(self.m_pyhouse_obj).House()
        self.assertEqual(l_pyh.Name, 'Test House')
        self.assertEqual(l_pyh.Key, 0)
        self.assertEqual(l_pyh.Active, True)

    def test_01_Schedules(self):
        l_pyh = GetPyhouse(self.m_pyhouse_obj).Schedules()
        PrettyPrintAny(l_pyh, 'Schedules')
        self.assertEqual(l_pyh.Schedules, {})
        pass

# ## END DBK
