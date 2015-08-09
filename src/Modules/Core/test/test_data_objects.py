"""
@name:      PyHouse/src/Modules/Core/test/test_data_objects.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@note:      Created on Mar 22, 2014
@license:   MIT License
@summary:   test ?.

Passed all 2 tests - DBK - 2015-08-08

"""

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core import data_objects
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test(SetupMixin, unittest.TestCase):


    def setUp(self):
        # print('Setup')
        pass

    def test_001_Load(self):
        pass

    def test_002_houses(self):
        pass

    def Xtest_003_house(self):
        pass

    def Xtest_004_name(self):
        l_house = self.m_pyhouse_obj.House
        l_name = l_house.Name
        self.assertEqual(l_name, 'Test House #1')

    def Xtest_005_street(self):
        l_data = self.m_pyhouse_obj
        l_house = l_data.House
        l_location = l_house.Location
        l_street = l_location.Street
        self.assertEqual(l_street, '5191 N Pink Poppy Dr')

# ## END DBK
