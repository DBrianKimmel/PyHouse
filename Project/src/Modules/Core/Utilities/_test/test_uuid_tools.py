"""
@name:      Modules/Core/Utilities/_test/test_uuid_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 22, 2015
@Summary:

Passed 8 of 9 tests - DBK - 2019-09-15

"""

__updated__ = '2019-09-15'

#  Import system type stuff
from twisted.trial import unittest

#  Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities import uuid_tools
from Modules.Core.Utilities.uuid_tools import Uuid
from Modules.Core.data_objects import UuidData

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


#  Import PyMh files and modules.
class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_uuid_tools')


class B1_Defs(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_File(self):
        """ Fixed literal file name in _test to be sure it is exactly where we want it.
        """
        l_file = uuid_tools._file_name(self.m_pyhouse_obj, 'Computer.uuid')
        print('B1-01-A - File Name:{}'.format(l_file))
        # self.assertEqual(l_file, '/etc/pyhouse/Uuid/Computer.uuid')

    def test_02_Uuid(self):
        l_uuid = uuid_tools.get_uuid_file(self.m_pyhouse_obj, 'Computer')
        # print('B1-02-A - UUID:{}'.format(l_uuid))
        self.assertEqual(len(l_uuid), 36)
        self.assertEqual(l_uuid[8:9], '-')
        self.assertEqual(l_uuid[13:14], '-')
        self.assertEqual(l_uuid[18:19], '-')
        self.assertEqual(l_uuid[23:24], '-')


class B2_UUID(SetupMixin, unittest.TestCase):
    """
    This series tests the complex PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self)

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
        # print(PrettyFormatAny.form(self.m_pyhouse_obj._Uuids, 'B2-04-A - one'))
        self.assertEqual(self.m_pyhouse_obj._Uuids.All[l_obj_0.UUID].UuidType, l_obj_0.UuidType)
        #
        l_obj_1 = UuidData()
        l_obj_1.UUID = '01234567-dead-beef-dead-fedcba987654'
        l_obj_1.UuidType = 'Room'
        Uuid.add_uuid(self.m_pyhouse_obj, l_obj_1)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj._Uuids.All, 'B2-04-B - two'))
        self.assertEqual(self.m_pyhouse_obj._Uuids.All[l_obj_1.UUID].UuidType, l_obj_1.UuidType)


class B3_File(SetupMixin, unittest.TestCase):
    """This tests reading and writing of uuid files in the /etc/pyhouse directory
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Read(self):
        pass

    def test_02_Write(self):
        pass

#  ## END DBK
