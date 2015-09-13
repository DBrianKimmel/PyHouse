"""
@name:      PyHouse/src/Modules/Lighting/test/test_lighting_actions.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep 3, 2015
@Summary:

"""

# Import system type stuff
import datetime
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
# from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A1_Api(SetupMixin, unittest.TestCase):
    """
    Test Staticmethods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_DoSchedule(self):
        pass
        self.assertEqual(l_delta, datetime.timedelta(0, 45296))

    def test_02_ChangeLight(self):
        pass
        self.assertEqual(l_delta, datetime.timedelta(0, 45296))

# ## END DBK
