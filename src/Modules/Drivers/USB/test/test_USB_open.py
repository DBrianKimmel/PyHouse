"""
@name:      PyHouse/src/Modules/Drivers/USB/test/test_USB_open.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 15, 2015
@Summary:

Passed all 1 tests - DBK - 2018-02-13

"""

__updated__ = '2018-02-13'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_version = '1.4.0'


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_USB_open')

# ## END DBK
