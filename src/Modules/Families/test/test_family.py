"""
@name:      PyHouse/src/Modules/Families/test/test_family.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@note:      Created on May 17, 2013
@license:   MIT License
@summary:   This module is for testing family.

Passed all 12 tests.  DBK 2014-08-23
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Families import family
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = family.API(self.m_pyhouse_obj)


class A1_Valid(SetupMixin, unittest.TestCase):
    """ This section tests the test environment to be valid bedore testing the "Real" stuff.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_ValidFamilies(self):
        PrettyPrintAny(family.VALID_FAMILIES, 'ValidFamilies')
        self.assertEqual(family.VALID_FAMILIES[0], 'Insteon')
        self.assertEqual(family.VALID_FAMILIES[1], 'UPB')
        self.assertEqual(family.VALID_FAMILIES[2], 'X10')

    def test_02_PyHouseObj(self):
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse Obj')
        PrettyPrintAny(self.m_pyhouse_obj.APIs, "PyHouse Obj API's")


class B1_One(SetupMixin, unittest.TestCase):
    """ This section tests the "Utility" class
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_family_obj = family.Utility._build_one_family_data('Insteon', 0)

    def test_01_BuildData(self):
        PrettyPrintAny(self.m_family_obj, "FamilyObj")
        self.assertEqual(self.m_family_obj.Name, 'Insteon')
        self.assertEqual(self.m_family_obj.Key, 0)
        self.assertEqual(self.m_family_obj.Active, True)
        self.assertEqual(self.m_family_obj.FamilyDeviceModuleName, 'Insteon_device')
        self.assertEqual(self.m_family_obj.FamilyPackageName, 'Modules.Families.Insteon')
        self.assertEqual(self.m_family_obj.FamilyXmlModuleName, 'Insteon_xml')

    def test_02_ImportOneMod(self):
        l_module = family.Utility._import_one_module(self.m_family_obj)
        PrettyPrintAny(l_module, "Module")
        PrettyPrintAny(self.m_family_obj, "Family")

    def test_03_InitMod(self):
        l_module = family.Utility._import_one_module(self.m_family_obj)
        l_xxx = family.Utility._initialize_one_module(self.m_pyhouse_obj, l_module)
        PrettyPrintAny(l_xxx, "xxx")

    def test_04_ImportOneXml(self):
        l_modXml = family.Utility._import_one_moduleXml(self.m_family_obj)
        PrettyPrintAny(l_modXml, "ModuleXml")

    def test_05_ImportOneXml(self):
        l_modXml = family.Utility._import_one_moduleXml(self.m_family_obj)
        PrettyPrintAny(l_modXml, "ModuleXml")


class B2_One(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_family_obj = family.Utility._build_one_family_data('Insteon', 0)

    def test_01_Import(self):
        l_obj = family.Utility._import_one_module(self.m_family_obj)
        # self.assertNotEqual(l_family_obj.API, None)
        PrettyPrintAny(l_obj, 'Insteon')

    def test_02_ImportXml(self):
        l_obj = family.Utility._import_one_moduleXml(self.m_family_obj)
        PrettyPrintAny(l_obj, 'Insteon')


class C1_API(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BuildFamily(self):
        l_family_obj = self.m_api.build_lighting_family_info(self.m_pyhouse_obj)
        PrettyPrintAny(l_family_obj, 'Family_Obj')
        l_ret = self.m_api._import_one_module(self.m_family_obj)
        PrettyPrintAny(l_ret, '')
        # PrettyPrintAny(l_family_obj['Insteon'], 'Family_Obj')
        self.assertNotEqual(l_ret, None, 'Error importing module Insteon')

    def test_02_start_family(self):
        PrettyPrintAny(self.m_family_obj, 'Insteon_Obj')
        l_ret = self.m_api._import_one_module(self.m_pyhouse_obj, self.m_family_obj)
        self.assertNotEqual(l_ret, None, 'Error importing module Insteon')

    def test_03_stop_family(self):
        l_ret = self.m_api._import_one_module(self.m_pyhouse_obj, self.m_family_obj)
        self.assertNotEqual(l_ret, None, 'Error importing module Insteon')

# ## END DBK
