"""
@name:      PyHouse/src/Modules/Computer/Web/_test/test_root_menu.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2013-2017 by D. Brian Kimmel
@note:      Created on Jul 12, 2013
@license:   MIT License
@summary:   Handle the home lighting system automation.

Passed all 2 tests - DBK - 2017-01-11
"""

__updated__ = '2017-01-11'

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from test import xml_data
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_root_menu')


class Test_02_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))




# ## END DBK
