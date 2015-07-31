"""
@name:      PyHouse/src/Modules/Families/test/test_family.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@note:      Created on May 17, 2013
@license:   MIT License
@summary:   This module is for testing family.

Passed all 12 tests.  DBK 2015-07-21
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Families import family
from Modules.Families.family import Utility, API as familyAPI
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_families = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()


class A1_Valid(SetupMixin, unittest.TestCase):
    """ This section tests the test environment to be valid bedore testing the "Real" stuff.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_ValidFamilies(self):
        # PrettyPrintAny(family.VALID_FAMILIES, 'ValidFamilies')
        self.assertEqual(family.VALID_FAMILIES[0], 'Insteon')
        self.assertEqual(family.VALID_FAMILIES[1], 'UPB')
        self.assertEqual(family.VALID_FAMILIES[2], 'X10')

    def test_02_PyHouseObj(self):
        # PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse Obj')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection')
        self.assertEqual(self.m_xml.controller.tag, 'Controller')

    def test_03_XML(self):
        # PrettyPrintAny(self.m_xml, "XML")
        pass

    def test_04_Families(self):
        # PrettyPrintAny(self.m_families, "m_families")
        pass

    def test_05_FamiliesInsteon(self):
        # PrettyPrintAny(self.m_families['Insteon'], "m_families['Insteon']")
        pass

    def test_06_FamiliesNull(self):
        # PrettyPrintAny(self.m_families['Null'], "m_families['Null']")
        pass

    def test_07_FamiliesUPB(self):
        # PrettyPrintAny(self.m_families['UPB'], "m_families['UPB']")
        pass

    def test_08_FamiliesX10(self):
        # PrettyPrintAny(self.m_families['X10'], "m_families['X10']")
        pass


class B1_One(SetupMixin, unittest.TestCase):
    """ This section tests the "Utility" class
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_family_obj = Utility._build_one_family_data(self.m_pyhouse_obj, 'Insteon')

    def test_01_Import(self):
        l_mod = Utility._do_import(self.m_family_obj, 'Insteon_xml')
        # PrettyPrintAny(self.m_family_obj, "FamilyObj")
        self.assertEqual(self.m_family_obj.Name, 'Insteon')
        self.assertEqual(self.m_family_obj.Key, 0)
        self.assertEqual(self.m_family_obj.Active, True)
        self.assertEqual(self.m_family_obj.FamilyDeviceModuleName, 'Insteon_device')
        self.assertEqual(self.m_family_obj.FamilyPackageName, 'Modules.Families.Insteon')
        self.assertEqual(self.m_family_obj.FamilyXmlModuleName, 'Insteon_xml')


class B2_One(SetupMixin, unittest.TestCase):
    """ This section tests the "Utility" class
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_family_obj = family.Utility._build_one_family_data(self.m_pyhouse_obj, 'Insteon')

    def test_01_BuildData(self):
        # PrettyPrintAny(self.m_family_obj, "FamilyObj")
        self.assertEqual(self.m_family_obj.Name, 'Insteon')
        self.assertEqual(self.m_family_obj.Key, 0)
        self.assertEqual(self.m_family_obj.Active, True)
        self.assertEqual(self.m_family_obj.FamilyDeviceModuleName, 'Insteon_device')
        self.assertEqual(self.m_family_obj.FamilyPackageName, 'Modules.Families.Insteon')
        self.assertEqual(self.m_family_obj.FamilyXmlModuleName, 'Insteon_xml')

    def test_02_ImportOneMod(self):
        l_module = family.Utility._init_component_apis(self.m_pyhouse_obj)
        # PrettyPrintAny(l_module, "Module")
        # PrettyPrintAny(self.m_family_obj, "Family")


class B3_One(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_family_obj = family.Utility._build_one_family_data(self.m_pyhouse_obj, 'Insteon')

    def test_01_Import(self):
        l_obj = family.Utility._init_component_apis(self.m_pyhouse_obj)
        # self.assertNotEqual(l_family_obj.API, None)
        # PrettyPrintAny(l_obj, 'Insteon')

# ## END DBK
