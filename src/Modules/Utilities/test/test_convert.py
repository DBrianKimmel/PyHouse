"""
@name: PyHouse/src/Modules/Utilities/test/test_convert.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2013-2016 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 4, 2013
@summary: This module is for testing conversion tools.

Passed all 5 tests - DBK - 2016-11-22
"""

__updated__ = '2016-11-22'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Utilities import convert
from test import xml_data
from test.testing_mixin import SetupPyHouseObj


STR_IPV4 = '192.168.1.54'
LONG_IPV4 = 3232235830L
STR_IPV6 = '2001:db8::1'
LONG_IPV6 = 42540766411282592856903984951653826561L


class SetupMixin(object):
    """
    Set up pyhouse_obj and xml element pointers
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)



class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_convert')


class B1_Convert(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_reactor = self.m_pyhouse_obj.Twisted.Reactor
        self.m_api = convert

    def test_01_Str2Long(self):
        l_long = self.m_api.str_to_long(STR_IPV4)
        self.assertEqual(l_long, LONG_IPV4)

    def test_02_Str2Long(self):
        l_long = self.m_api.str_to_long(STR_IPV6)
        self.assertEqual(l_long, LONG_IPV6)

    def test_03_Long2Str(self):
        l_long = self.m_api.long_to_str(LONG_IPV4)
        self.assertEqual(l_long, STR_IPV4)

    def test_04_Long2Str(self):
        l_long = self.m_api.long_to_str(LONG_IPV6)
        self.assertEqual(l_long, STR_IPV6)

# ## END
