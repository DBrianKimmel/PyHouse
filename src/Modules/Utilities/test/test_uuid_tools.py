"""
@name:      PyHouse/src/Modules/Utilities/test/test_uuid_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 22, 2015
@Summary:

Passed all 3 tests - DBK - 2015-07-24

"""

#  Import system type stuff
from twisted.trial import unittest

from Modules.Utilities.uuid_tools import Uuid, FileUuid
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG
import xml.etree.ElementTree as ET


#  Import PyMh files and modules.
class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A1_UUID(SetupMixin, unittest.TestCase):
    """
    This series tests the complex PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_None(self):
        l_test = None
        l_uuid = Uuid.make_valid(l_test)
        #  print('UUID = {}'.format(l_uuid))
        self.assertNotEqual(l_uuid, l_test)

    def test_02_Invalid(self):
        l_test = '123456'
        l_uuid = Uuid.make_valid(l_test)
        #  print('UUID = {}'.format(l_uuid))
        self.assertNotEqual(l_uuid, l_test)

    def test_03_Valid(self):
        l_test = '12345678-dead-beef-dead-fedcba987654'
        l_uuid = Uuid.make_valid(l_test)
        #  print('UUID = {}'.format(l_uuid))
        self.assertEqual(l_uuid, l_test)


class A2_File(SetupMixin, unittest.TestCase):
    """This tests reading and writing of uuid files in the /etc/pyhouse directory
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Read(self):
        FileUuid().read_file('Computer')

    def test_02_Write(self):
        FileUuid().write_file('Computer')
        pass

#  ## END DBK
