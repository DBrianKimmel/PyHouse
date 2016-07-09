"""
@name:      PyHouse/src/Modules/Utilities/test/test_uuid_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 22, 2015
@Summary:

Passed all 6 tests - DBK - 2016-07-09

"""

__updated__ = '2016-07-09'

#  Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

#  Import PyMh files
from Modules.Core.data_objects import UuidData
from Modules.Utilities.debug_tools import PrettyFormatAny
from Modules.Utilities.uuid_tools import Uuid, FileUuid
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG


#  Import PyMh files and modules.
class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class B1_UUID(SetupMixin, unittest.TestCase):
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

    def test_04_Add(self):
        l_obj_0 = UuidData()
        l_obj_0.UUID = '12345678-dead-beef-dead-fedcba987654'
        l_obj_0.UuidType = 'House'
        Uuid.add_uuid(self.m_pyhouse_obj, l_obj_0)
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Uuids, 'B1-4-A - one'))
        self.assertEqual(self.m_pyhouse_obj.Uuids[l_obj_0.UUID].UuidType, l_obj_0.UuidType)
        #
        l_obj_1 = UuidData()
        l_obj_1.UUID = '01234567-dead-beef-dead-fedcba987654'
        l_obj_1.UuidType = 'Room'
        Uuid.add_uuid(self.m_pyhouse_obj, l_obj_1)
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Uuids, 'B1-4-B - two'))
        self.assertEqual(self.m_pyhouse_obj.Uuids[l_obj_1.UUID].UuidType, l_obj_1.UuidType)


class B2_File(SetupMixin, unittest.TestCase):
    """This tests reading and writing of uuid files in the /etc/pyhouse directory
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Read(self):
        FileUuid().XXXread_file('Computer')

    def test_02_Write(self):
        # FileUuid().XXXwrite_file('Computer')
        pass

#  ## END DBK
