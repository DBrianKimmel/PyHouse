"""
@name:      Modules/Families/_test/test_family.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@note:      Created on May 17, 2013
@license:   MIT License
@summary:   This module is for testing family.

Passed all 15 tests.  DBK 2019-02-21
"""

__updated__ = '2019-10-06'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
import importlib
import os

# Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj

from Modules.Families import family
from Modules.Families.family import \
    lightingUtility as familyUtil, \
    FamilyModuleInformation
from Modules.Families.test.xml_family import \
    TESTING_FAMILY_NAME_0, \
    TESTING_FAMILY_NAME_1, \
    TESTING_FAMILY_NAME_2, \
    TESTING_FAMILY_NAME_3
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        # self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_yaml = SetupPyHouseObj().BuildYaml(None)
        self.m_filename = 'families.yaml'
        # self.m_families = familyApi(self.m_pyhouse_obj).LoadFamilyTesting()

    def createFamilyObj(self):
        l_family_obj = FamilyModuleInformation()
        l_family_obj.Name = 'Insteon'
        l_family_obj.Key = 0
        l_family_obj.Active = True
        l_family_obj.FamilyPackageName = 'Modules.Families.Insteon'
        importlib.import_module(l_family_obj.FamilyPackageName)
        return l_family_obj


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_family')


class A1_Validate(SetupMixin, unittest.TestCase):
    """ This section tests the _test environment to be valid before testing the "Real" stuff.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Name(self):
        l_name = 'Insteon'
        print('Name: {}'.format(l_name))
        l_lc = l_name.lower()
        print('Name-lc: {}'.format(l_lc))
        l_cap = l_lc.capitalize()
        print('Name-cap: {}'.format(l_cap))

    def test_02_ValidFamiliesXml(self):
        """ Be sure the family names are what we expect later.
        """
        # print(PrettyFormatAny.form(family.VALID_FAMILIES, 'A1-02-A - Valid'))
        self.assertEqual(family.VALID_FAMILIES[0], TESTING_FAMILY_NAME_0)
        self.assertEqual(family.VALID_FAMILIES[1], TESTING_FAMILY_NAME_1)
        self.assertEqual(family.VALID_FAMILIES[2], TESTING_FAMILY_NAME_2)
        self.assertEqual(family.VALID_FAMILIES[3], TESTING_FAMILY_NAME_3)

    def test_05_Insteon(self):
        l_obj = familyUtil()._build_one_family_data(self.m_pyhouse_obj, 'Insteon')
        # print(PrettyFormatAny.form(l_obj, 'A1-05-A- Insteon'))
        self.assertEqual(l_obj.Name, TESTING_FAMILY_NAME_1)
        self.assertEqual(l_obj.FamilyDevice_ModuleName, 'Insteon_device')
        self.assertEqual(l_obj.FamilyPackageName, 'Modules.Families.Insteon')
        self.assertEqual(l_obj.FamilyXml_ModuleName, 'Insteon_xml')

    def test_06_UPB(self):
        l_obj = familyUtil()._build_one_family_data(self.m_pyhouse_obj, 'UPB')
        # print(PrettyFormatAny.form(l_obj, 'A1-06-A - UPB'))
        self.assertEqual(l_obj.Name, TESTING_FAMILY_NAME_2)
        self.assertEqual(l_obj.FamilyDevice_ModuleName, 'UPB_device')
        self.assertEqual(l_obj.FamilyPackageName, 'Modules.Families.UPB')
        self.assertEqual(l_obj.FamilyXml_ModuleName, 'UPB_xml')

    def test_07_X10(self):
        l_obj = familyUtil()._build_one_family_data(self.m_pyhouse_obj, 'X10')
        # print(PrettyFormatAny.form(l_obj, 'A1-07-A - X10'))
        self.assertEqual(l_obj.Name, TESTING_FAMILY_NAME_3)
        self.assertEqual(l_obj.FamilyDevice_ModuleName, 'X10_device')
        self.assertEqual(l_obj.FamilyPackageName, 'Modules.Families.X10')
        self.assertEqual(l_obj.FamilyXml_ModuleName, 'X10_xml')


class A4_ValidFamily(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Defined(self):
        """ Run thru the directories in the Family section of the source code.
        """
        for dirname, dirnames, filenames in os.walk('..'):
            # print path to all subdirectories first.
            for subdirname in dirnames:
                # print('Dirs: ', os.path.join(dirname, subdirname))
                pass

            # print path to all filenames.
            # for filename in filenames:
            #    print('Files: ', os.path.join(dirname, filename))

            # Advanced usage:
            # editing the 'dirnames' list will stop os.walk() from recursing into there.


class B1_One(SetupMixin, unittest.TestCase):
    """ This section tests the "lightingUtility" class
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Import(self):
        """
        """
        l_obj = familyUtil()._build_one_family_data(self.m_pyhouse_obj, 'Insteon')
        print(PrettyFormatAny.form(l_obj, 'B1-01-A - Module'))
        _l_mod = familyUtil()._do_import(l_obj, 'Insteon_xml')
        self.assertEqual(l_obj.Name, 'Insteon')
        self.assertEqual(l_obj.Key, 0)
        self.assertEqual(l_obj.Active, True)
        self.assertEqual(l_obj.FamilyDevice_ModuleName, 'Insteon_device')
        self.assertEqual(l_obj.FamilyPackageName, 'Modules.Families.Insteon')
        self.assertEqual(l_obj.FamilyXml_ModuleName, 'Insteon_xml')

    def test_02_Import(self):
        l_obj = familyUtil()._build_one_family_data(self.m_pyhouse_obj, 'UPB')
        _l_mod = familyUtil()._do_import(l_obj, 'UPB_xml')
        # print(PrettyFormatAny.form(l_mod, 'B1-02-A - Module'))
        self.assertEqual(l_obj.Name, 'UPB')
        self.assertEqual(l_obj.Key, 0)
        self.assertEqual(l_obj.Active, True)
        self.assertEqual(l_obj.FamilyDevice_ModuleName, 'UPB_device')
        self.assertEqual(l_obj.FamilyPackageName, 'Modules.Families.UPB')
        self.assertEqual(l_obj.FamilyXml_ModuleName, 'UPB_xml')


class B2_One(SetupMixin, unittest.TestCase):
    """ This section tests the "lightingUtility" class
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_family_obj = familyUtil()._build_one_family_data(self.m_pyhouse_obj, 'Insteon')

    def test_01_BuildData(self):
        self.assertEqual(self.m_family_obj.Name, 'Insteon')
        self.assertEqual(self.m_family_obj.Key, 0)
        self.assertEqual(self.m_family_obj.Active, True)
        self.assertEqual(self.m_family_obj.FamilyDevice_ModuleName, 'Insteon_device')
        self.assertEqual(self.m_family_obj.FamilyPackageName, 'Modules.Families.Insteon')
        self.assertEqual(self.m_family_obj.FamilyXml_ModuleName, 'Insteon_xml')

    def test_02_ImportOneMod(self):
        _l_module = familyUtil()._init_family_component_apis(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(_l_module, 'B2-02-A - Module'))
        pass


class B3_One(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_family_obj = familyUtil()._build_one_family_data(self.m_pyhouse_obj, 'Insteon')

    def test_01_Import(self):
        l_obj = familyUtil()._init_family_component_apis(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'B3-01-A - Module'))
        self.assertNotEqual(l_obj, None)


class C1_Import(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        # self.m_family_obj = familyUtil()._build_one_family_data(self.m_pyhouse_obj, 'Insteon')

    def test_01_Import(self):
        l_family_obj = self.createFamilyObj()
        l_mod = 'Insteon_device'
        # print(PrettyFormatAny.form(l_family_obj, 'C1-01-A - Module'))
        l_obj = familyUtil()._do_import(l_family_obj, l_mod)
        # print(PrettyFormatAny.form(l_obj, 'C1-01-B - Module'))
        self.assertNotEqual(l_obj, None)


class C2_API(SetupMixin, unittest.TestCase):
    """ This section tests the creation of an API reference
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_family_obj = familyUtil()._build_one_family_data(self.m_pyhouse_obj, 'Insteon')

    def test_01_Import(self):
        l_mod_name = 'Insteon_device'
        l_mod_ref = None
        l_obj = familyUtil()._create_api_instance(self.m_pyhouse_obj, l_mod_name, l_mod_ref)
        print(PrettyFormatAny.form(l_obj, 'C2-01-A - Module'))
        self.assertNotEqual(l_obj, None)


class D1_One(SetupMixin, unittest.TestCase):
    """ This section tests the creation of one family Data
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        # self.m_family_obj = familyUtil()._build_one_family_data(self.m_pyhouse_obj, 'Insteon')

    def test_01_Null(self):
        l_mod_name = 'Null'
        l_family_obj = familyUtil()._build_one_family_data(self.m_pyhouse_obj, l_mod_name)
        # print(PrettyFormatAny.form(l_family_obj, 'D1-01-A - Family'))
        self.assertEqual(l_family_obj.Name, l_mod_name)
        # self.assertNotEqual(l_obj, None)

    def test_02_Insteon(self):
        l_mod_name = 'Insteon'
        l_family_obj = familyUtil()._build_one_family_data(self.m_pyhouse_obj, l_mod_name)
        # print(PrettyFormatAny.form(l_family_obj, 'D1-02-A - Family'))
        self.assertEqual(l_family_obj.Name, l_mod_name)

# ## END DBK
