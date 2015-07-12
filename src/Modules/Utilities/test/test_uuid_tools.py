"""
@name:      PyHouse/src/Modules/Utilities/test/test_uuid_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 22, 2015
@Summary:

"""

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Utilities import uuid_tools
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A01_UUID(SetupMixin, unittest.TestCase):
    """
    This series tests the complex PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_None(self):
        l_uuid = uuid_tools.get_uuid(None)
        print('UUID = {}'.format(l_uuid))

    def test_02_Invalid(self):
        l_uuid = uuid_tools.get_uuid('123456')
        print('UUID = {}'.format(l_uuid))

    def test_03_Valid(self):
        l_uuid = uuid_tools.get_uuid('12345678-dead-beef-dead-fedcba987654')
        print('UUID = {}'.format(l_uuid))
        self.assertEqual(l_uuid, '12345678-dead-beef-dead-fedcba987654')

# ## END DBK
