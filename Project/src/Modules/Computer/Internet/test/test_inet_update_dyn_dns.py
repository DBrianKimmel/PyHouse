"""
@name:      PyHouse/src/Modules/Computer/Internet/test/test_inet_update_dyn_dns.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 27, 2014
@Summary:

Passed all 2 tests - DBK - 2018-02-12

"""

__updated__ = '2019-06-25'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj


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
        print('Id: test_inet_update_dyn_dns')


class Test(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_reactor = self.m_pyhouse_obj._Twisted.Reactor

    def testName(self):
        pass

# ## END DBK
