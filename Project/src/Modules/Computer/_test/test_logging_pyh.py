"""
@name:      PyHouse/src/Modules/Computer/_test/test_logging_pyh.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@note:      Created on Apr 30, 2014
@license:   MIT License
@summary:

Passed all 2 tests - DBK - 2016-11-21

"""

__updated__ = '2019-10-06'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core import logging_pyh as Logger
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
        print('Id: test_logging_pyh')


class Test_A1_SetupLogging(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = Logger.Api()
        self.m_api.read_xml(self.m_pyhouse_obj)
        self.LOG = Logger.getLogger('PyHouse.test_logging_pyh ')

    def test_0402_openDebug(self):
        pass

# ## END DBK
