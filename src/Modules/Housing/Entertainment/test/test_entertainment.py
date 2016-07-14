"""
@name:      PyHouse/src/Modules/Entertainment/test/test_entertainment.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 14, 2013
@summary:   Test

Passed all 1 tests - DBK - 2016-07-10

"""

__updated__ = '2016-07-10'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Tags'))
        self.assertEqual(self.m_pyhouse_obj.House.Rooms, None)

# ## END DBK
