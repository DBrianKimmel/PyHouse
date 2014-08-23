"""
@name: PyHouse/src/Modules/Families/test/test_family.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@note: Created on May 17, 2013
@license: MIT License
@summary: This module is for testing family.

Passed all 12 tests.  DBK 2014-08-23
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Families import family
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_01_Valid(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = family.API()
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()

    def test_0201_ValidFamilies(self):
        self.assertEqual(family.VALID_FAMILIES[0], 'Insteon')
        self.assertEqual(family.VALID_FAMILIES[1], 'UPB')
        self.assertEqual(family.VALID_FAMILIES[2], 'X10')


class Test_02_Utility(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = family.API()
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()

    def test_0211_BuildOne(self):
        l_family_obj = self.m_api._build_one_family_data('Insteon')
        PrettyPrintAny(l_family_obj)
        self.assertEqual(l_family_obj.Name, 'Insteon', 'Invalid name')
        self.assertEqual(l_family_obj.FamilyDeviceModuleName, 'Insteon_device', 'Invalid Device Module Name')
        self.assertEqual(l_family_obj.FamilyPackageName, 'Modules.Families.Insteon', 'Invalid Package Name')

    def test_0212_BuildOne(self):
        l_family_obj = self.m_api._build_one_family_data('UPB')
        PrettyPrintAny(l_family_obj)
        self.assertEqual(l_family_obj.Name, 'UPB', 'Invalid name')
        self.assertEqual(l_family_obj.FamilyDeviceModuleName, 'UPB_device', 'Invalid Device Module Name')
        self.assertEqual(l_family_obj.FamilyPackageName, 'Modules.Families.UPB', 'Invalid Package Name')

    def test_0213_BuildOne(self):
        l_family_obj = self.m_api._build_one_family_data('X10')
        PrettyPrintAny(l_family_obj, 'X10')
        self.assertEqual(l_family_obj.Name, 'X10', 'Invalid name')
        self.assertEqual(l_family_obj.FamilyDeviceModuleName, 'X10_device', 'Invalid Device Module Name')
        self.assertEqual(l_family_obj.FamilyPackageName, 'Modules.Families.X10', 'Invalid Package Name')

    def test_0214_BuildOne(self):
        l_family_obj = self.m_api._build_one_family_data('Null')
        PrettyPrintAny(l_family_obj, 'Null')
        self.assertEqual(l_family_obj.Name, 'Null', 'Invalid name')
        self.assertEqual(l_family_obj.FamilyDeviceModuleName, 'Null_device', 'Invalid Device Module Name')
        self.assertEqual(l_family_obj.FamilyPackageName, 'Modules.Families.Null', 'Invalid Package Name')

    def test_0221_ImportOne(self):
        l_obj = self.m_api._build_one_family_data('Insteon')
        l_family_obj, l_xml_obj = self.m_api._import_one_module(l_obj)
        self.assertNotEqual(l_family_obj.API, None, 'Error importing module Insteon')
        PrettyPrintAny(l_family_obj, 'Insteon')

    def test_0222_ImportOne(self):
        l_obj = self.m_api._build_one_family_data('UPB')
        l_family_obj = self.m_api._import_one_module(l_obj)
        self.assertNotEqual(l_family_obj, None, 'Error importing module UPB')
        PrettyPrintAny(l_family_obj, 'Upb')

    def test_0223_ImportOne(self):
        l_obj = self.m_api._build_one_family_data('X10')
        l_family_obj = self.m_api._import_one_module(l_obj)
        self.assertNotEqual(l_family_obj, None, 'Error importing module X10')
        PrettyPrintAny(l_family_obj, 'X10')

    def test_0224_ImportOne(self):
        l_obj = self.m_api._build_one_family_data('Null')
        l_family_obj = self.m_api._import_one_module(l_obj)
        self.assertNotEqual(l_family_obj, None, 'Error importing module Null')
        PrettyPrintAny(l_family_obj, 'Null')


class Test_03_API(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = family.API()
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()

    def test_0311_BuildFamily(self):
        l_family_obj = self.m_api.build_lighting_family_info()
        PrettyPrintAny(l_family_obj, 'Family_Obj')
        l_family_obj = self.m_api._build_one_family_data('Insteon')
        l_ret = self.m_api._import_one_module(l_family_obj)
        self.assertNotEqual(l_ret, None, 'Error importing module Insteon')
        pass

    def test_0341_start_family(self):
        l_family_obj = self.m_api.build_lighting_family_info()
        l_insteon_obj = self.m_api._build_one_family_data('Insteon')
        PrettyPrintAny(l_insteon_obj, 'Insteon_Obj')
        l_ret = self.m_api._import_one_module(l_family_obj)
        self.assertNotEqual(l_ret, None, 'Error importing module Insteon')
        pass

    def test_0361_stop_family(self):
        l_family_obj = self.m_api._build_one_family_data('Insteon')
        l_ret = self.m_api._import_one_module(l_family_obj)
        self.assertNotEqual(l_ret, None, 'Error importing module Insteon')
        pass

# ## END DBK
