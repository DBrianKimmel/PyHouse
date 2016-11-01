"""
@name:      /home/briank/PyHouse/src/Modules/Families/Insteon/test/test_Insteon_Hub.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Oct 27, 2016
@summary:   Test

Passed all 2 tests - DBK - 2015-10-31

"""

__updated__ = '2016-10-31'

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG


class SetupMixin(object):
    """ Set up pyhouse object
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_Insteon_xml')


class A1_Prep(SetupMixin, unittest.TestCase):
    """ This section tests the setup
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_device = None

# ## END DBK
