"""
@name:      PyHouse/src/Modules/Families/test/test_family.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2018 by D. Brian Kimmel
@note:      Created on May 17, 2013
@license:   MIT License
@summary:   This module is for testing family.

Passed all 13 tests.  DBK 2018-01-22
"""

__updated__ = '2018-01-22'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Families import family
from Modules.Families.family import Utility, API as familyAPI
from Modules.Families.test.xml_family import \
    TESTING_FAMILY_NAME_0, \
    TESTING_FAMILY_NAME_1, \
    TESTING_FAMILY_NAME_2, \
    TESTING_FAMILY_NAME_3
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_families = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_family')


class A1_Valid(SetupMixin, unittest.TestCase):
    """ This section tests the test environment to be valid before testing the "Real" stuff.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_ValidFamilies(self):
        """ Be sure the family names are what we expect later.
        """
        # print(PrettyFormatAny.form(family.VALID_FAMILIES, 'A1-01-A - Valid'))
        self.assertEqual(family.VALID_FAMILIES[0], TESTING_FAMILY_NAME_0)
        self.assertEqual(family.VALID_FAMILIES[1], TESTING_FAMILY_NAME_1)
        self.assertEqual(family.VALID_FAMILIES[2], TESTING_FAMILY_NAME_2)
        self.assertEqual(family.VALID_FAMILIES[3], TESTING_FAMILY_NAME_3)

    def test_02_PyHouseObj(self):
        """ Be sure that m_xml is set up properly
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Xml'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.lighting_sect.tag, 'LightingSection')
        self.assertEqual(self.m_xml.button_sect.tag, 'ButtonSection')
        self.assertEqual(self.m_xml.button.tag, 'Button')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection')
        self.assertEqual(self.m_xml.controller.tag, 'Controller')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection')
        self.assertEqual(self.m_xml.light.tag, 'Light')

    def test_03_XML(self):
        # print(PrettyFormatAny.form(XML_LONG, 'XML))
        pass

    def test_04_FamiliesNull(self):
        l_obj = Utility._build_one_family_data(self.m_pyhouse_obj, 'Null')
        # print(PrettyFormatAny.form(l_obj, 'A1-04-A - Null'))
        self.assertEqual(l_obj.Name, TESTING_FAMILY_NAME_0)
        self.assertEqual(l_obj.FamilyDeviceModuleName, 'Null_device')
        self.assertEqual(l_obj.FamilyPackageName, 'Modules.Families.Null')
        self.assertEqual(l_obj.FamilyXmlModuleName, 'Null_xml')

    def test_05_FamiliesInsteon(self):
        l_obj = Utility._build_one_family_data(self.m_pyhouse_obj, 'Insteon')
        # print(PrettyFormatAny.form(l_obj, 'A1-05-A- Insteon'))
        self.assertEqual(l_obj.Name, TESTING_FAMILY_NAME_1)
        self.assertEqual(l_obj.FamilyDeviceModuleName, 'Insteon_device')
        self.assertEqual(l_obj.FamilyPackageName, 'Modules.Families.Insteon')
        self.assertEqual(l_obj.FamilyXmlModuleName, 'Insteon_xml')

    def test_06_FamiliesUPB(self):
        l_obj = Utility._build_one_family_data(self.m_pyhouse_obj, 'UPB')
        # print(PrettyFormatAny.form(l_obj, 'A1-06-A - UPB'))
        self.assertEqual(l_obj.Name, TESTING_FAMILY_NAME_2)
        self.assertEqual(l_obj.FamilyDeviceModuleName, 'UPB_device')
        self.assertEqual(l_obj.FamilyPackageName, 'Modules.Families.UPB')
        self.assertEqual(l_obj.FamilyXmlModuleName, 'UPB_xml')

    def test_07_FamiliesX10(self):
        l_obj = Utility._build_one_family_data(self.m_pyhouse_obj, 'X10')
        # print(PrettyFormatAny.form(l_obj, 'A1-07-A - X10'))
        self.assertEqual(l_obj.Name, TESTING_FAMILY_NAME_3)
        self.assertEqual(l_obj.FamilyDeviceModuleName, 'X10_device')
        self.assertEqual(l_obj.FamilyPackageName, 'Modules.Families.X10')
        self.assertEqual(l_obj.FamilyXmlModuleName, 'X10_xml')


class B1_One(SetupMixin, unittest.TestCase):
    """ This section tests the "Utility" class
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Import(self):
        self.m_family_obj = Utility._build_one_family_data(self.m_pyhouse_obj, 'Insteon')
        l_mod = Utility._do_import(self.m_family_obj, 'Insteon_xml')
        # print(PrettyFormatAny.form(l_mod, 'B1-01-A - Module'))
        self.assertEqual(self.m_family_obj.Name, 'Insteon')
        self.assertEqual(self.m_family_obj.Key, 0)
        self.assertEqual(self.m_family_obj.Active, True)
        self.assertEqual(self.m_family_obj.FamilyDeviceModuleName, 'Insteon_device')
        self.assertEqual(self.m_family_obj.FamilyPackageName, 'Modules.Families.Insteon')
        self.assertEqual(self.m_family_obj.FamilyXmlModuleName, 'Insteon_xml')

    def test_02_Import(self):
        self.m_family_obj = Utility._build_one_family_data(self.m_pyhouse_obj, 'UPB')
        l_mod = Utility._do_import(self.m_family_obj, 'UPB_xml')
        # print(PrettyFormatAny.form(l_mod, 'B1-02-A - Module'))
        self.assertEqual(self.m_family_obj.Name, 'UPB')
        self.assertEqual(self.m_family_obj.Key, 0)
        self.assertEqual(self.m_family_obj.Active, True)
        self.assertEqual(self.m_family_obj.FamilyDeviceModuleName, 'UPB_device')
        self.assertEqual(self.m_family_obj.FamilyPackageName, 'Modules.Families.UPB')
        self.assertEqual(self.m_family_obj.FamilyXmlModuleName, 'UPB_xml')


class B2_One(SetupMixin, unittest.TestCase):
    """ This section tests the "Utility" class
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_family_obj = family.Utility._build_one_family_data(self.m_pyhouse_obj, 'Insteon')

    def test_01_BuildData(self):
        self.assertEqual(self.m_family_obj.Name, 'Insteon')
        self.assertEqual(self.m_family_obj.Key, 0)
        self.assertEqual(self.m_family_obj.Active, True)
        self.assertEqual(self.m_family_obj.FamilyDeviceModuleName, 'Insteon_device')
        self.assertEqual(self.m_family_obj.FamilyPackageName, 'Modules.Families.Insteon')
        self.assertEqual(self.m_family_obj.FamilyXmlModuleName, 'Insteon_xml')

    def test_02_ImportOneMod(self):
        l_module = family.Utility._init_component_apis(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_module, 'Module'))


class B3_One(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_family_obj = family.Utility._build_one_family_data(self.m_pyhouse_obj, 'Insteon')

    def test_01_Import(self):
        l_obj = family.Utility._init_component_apis(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'B3-01-A - Module'))
        self.assertNotEqual(l_obj, None)

# ## END DBK
