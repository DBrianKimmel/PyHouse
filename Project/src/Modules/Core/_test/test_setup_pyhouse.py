"""
@name:      PyHouse/Project/src/Modules/Core/_test/test_setup_pyhouse.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2020 by D. Brian Kimmel
@note:      Created on Mar 2, 2014
@license:   MIT License
@summary:   This module sets up the Core part of PyHouse.

Passed all 19 tests - DBK - 2019-06-18
"""

__updated__ = '2020-02-10'

# Import system type stuff
import os
from twisted.trial import unittest

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities.uuid_tools import Uuid as toolUuid
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Computer.computer import ComputerInformation, ComputerApis
from Modules.House import HouseInformation
from Modules.Core.setup_pyhouse_obj import TwistedInformation


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()


class A0(unittest.TestCase):

    def test_00_Print(self):
        print('Id: test_setup_pyhouse')
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the _test
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_PyHouseObj(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        print(PrettyFormatAny.form(self.m_pyhouse_obj._Config, 'A1-01-A - PyHouse.Xml'))
        self.assertNotEqual(self.m_pyhouse_obj._Config, None)


class B1_UUIDs(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def _build_file(self, p_pyhouse_obj, p_filename):
        l_file = os.path.join(p_pyhouse_obj.Xml.XmlConfigDir, p_filename)
        return l_file

    def _read_file(self, p_pyhouse_obj, p_filename):
        l_name = self._build_file(p_pyhouse_obj, p_filename)
        try:
            l_file = open(l_name, 'r')
            l_ret = l_file.read()
        except IOError:
            l_ret = toolUuid.create_uuid()
        return l_ret


def _write_file(self, p_pyhouse_obj, p_filename, p_uuid):
    l_name = self._build_file(p_pyhouse_obj, p_filename)
    try:
        l_file = open(l_name, 'w')
        l_ret = l_file.write(p_uuid)
    except IOError as e_err:
        l_ret = e_err
    return l_ret

    def test_01_Xml(self):
        l_xml = self.m_pyhouse_obj.Xml
        # print(PrettyFormatAny.form(l_xml, 'PyHouse,Xml'))
        self.assertEqual(l_xml.XmlConfigDir, '/etc/pyhouse/')

    def test_02_build(self):
        """
        """
        l_file = self._build_file(self.m_pyhouse_obj, 'Computer.uuid')
        self.assertEqual(l_file, '/etc/pyhouse/Computer.uuid')

    def test_03_Read(self):
        _l_uuid = self._read_file(self.m_pyhouse_obj, 'Computer.uuid')
        # print('B1-03-A - UUID: {}'.format(l_uuid))

    def test_04_Write(self):
        l_uuid = '222ec0e9-d76e-11e6-b40f-74dfbfae5aed'
        _l_ret = self._write_file(self.m_pyhouse_obj, 'Computer.uuid', l_uuid)
        # print('B1-03-A - UUID: {}'.format(l_ret))


class C1_Structures(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_PyHouse(self):
        """ Test every component of PyHouseInformation()
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'C1-1-A PyHouse obj'))
        self.assertIsInstance(self.m_pyhouse_obj.Computer, ComputerInformation)
        self.assertIsInstance(self.m_pyhouse_obj.House, HouseInformation)
        self.assertIsInstance(self.m_pyhouse_obj._Twisted, TwistedInformation)
        self.assertEqual(self.m_pyhouse_obj._Uuids.All, {})

    def test_02_Apis(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj._Apis, 'C1-2-A PyHouse Apis'))
        self.assertIsInstance(self.m_pyhouse_obj._Apis.Computer, ComputerApis)

    def test_03_Computer(self):
        # sprint(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'C1-3-A PyHouse.Computer obj'))
        pass

    def test_04_House(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'C1-4-A PyHouse.House obj'))
        pass

    def test_05_Services(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'C1-1-A PyHouse obj'))
        pass

    def test_06_Twisted(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj._Twisted, 'C1-6-A PyHouse._Twisted obj'))
        pass

    def test_07_Uuids(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj._Uuids, 'C1-7-A PyHouse._Uuids obj'))
        pass

    def test_08_Xml(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Xml, 'C1-8-A PyHouse.Xml obj'))
        pass

# ## END DBK
