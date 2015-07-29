"""
@name:      PyHouse/src/Modules/families/Null/test/test_Null_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2015 by briank
@license:   MIT License
@note:      Created on Aug 10, 2014
@Summary:

Passed all 1 tests - DBK - 2015-07-28

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
# from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class C01_API(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def tearDown(self):
        pass

    def testName(self):
        pass

# ## END DBK
