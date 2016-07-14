"""
@name:      PyHouse/src/Modules/entertain/test/test_pandora.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 22, 2014
@summary:   Test

"""

__updated__ = '2016-07-11'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny
from test.xml_data import XML_LONG
from Modules.Entertainment.onkyo import API as onkyoApi


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testName(self):
        pass


class B1_Init(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local
        module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_read_xml(self):
        l_api = onkyoApi(self.m_pyhouse_obj)
        l_obj = l_api.LoadXml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_obj, 'B1-1-A - Flag'))
        # self.assertEqual(l_pyhouse.tag, 'PyHouse')

# ## END DBK
