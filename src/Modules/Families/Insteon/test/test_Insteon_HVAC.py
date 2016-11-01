"""
@name:      PyHouse/src/Modules/Families/Insteon/test/test_Insteon_HVAC.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 6, 2014
@Summary:

Passed all 2 tests - DBK - 2015-07-29

"""

__updated__ = '2016-10-31'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
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
        print('Id: test_Insteon_HVAC')


class C01_Util(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Class(self):
        pass
        # Insteon_HVAC.Util().get_device_obj(self.m_pyhouse_obj, 'xxx')

# ## END DBK
