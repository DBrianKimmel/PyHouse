"""
@name: PyHouse/src/Modules/Families/test/test_family.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
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
from test.xml_data import *
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny



class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)



class C01_Valid(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = family.API()
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()

    def test_01_ValidFamilies(self):
        self.assertEqual(family.VALID_FAMILIES[0], 'Insteon')
        self.assertEqual(family.VALID_FAMILIES[1], 'UPB')
        self.assertEqual(family.VALID_FAMILIES[2], 'X10')



class C02_Utility(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = family.API()
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_family_obj = family.Utility._build_one_family_data('Insteon', 0)

    def test_01_BuildOne(self):
        PrettyPrintAny(self.m_family_obj)
        self.assertEqual(self.m_family_obj.Name, 'Insteon', 'Invalid name')
        self.assertEqual(self.m_family_obj.FamilyDeviceModuleName, 'Insteon_device', 'Invalid Device Module Name')
        self.assertEqual(self.m_family_obj.FamilyPackageName, 'Modules.Families.Insteon', 'Invalid Package Name')

    def test_02_ImportOne(self):
        l_family_obj, l_xml_obj = family.Utility._import_one_module(self.m_family_obj)
        self.assertNotEqual(l_family_obj.API, None, 'Error importing module Insteon')
        PrettyPrintAny(l_family_obj, 'Insteon')
        PrettyPrintAny(l_xml_obj, 'XML')

    def test_03_InitializeOne(self):
        pass



class C03_API(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = family.API()
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_family_obj = family.Utility._build_one_family_data('Insteon', 0)

    def test_01_BuildFamily(self):
        l_family_obj = self.m_api.build_lighting_family_info()
        l_ret = self.m_api._import_one_module(self.m_family_obj)
        PrettyPrintAny(l_family_obj, 'Family_Obj')
        PrettyPrintAny(l_family_obj['Insteon'], 'Family_Obj')
        PrettyPrintAny(l_ret, '')
        self.assertNotEqual(l_ret, None, 'Error importing module Insteon')

    def test_02_start_family(self):
        PrettyPrintAny(self.m_family_obj, 'Insteon_Obj')
        l_ret = self.m_api._import_one_module(self.m_family_obj)
        self.assertNotEqual(l_ret, None, 'Error importing module Insteon')

    def test_03_stop_family(self):
        l_ret = self.m_api._import_one_module(self.m_family_obj)
        self.assertNotEqual(l_ret, None, 'Error importing module Insteon')

# ## END DBK
