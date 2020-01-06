"""
@name:      Modules/House/Family/_test/test_family.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@note:      Created on May 17, 2013
@license:   MIT License
@summary:   This module is for testing family.

Passed all 15 tests.  DBK 2019-02-21
"""

__updated__ = '2019-11-04'

# Import system type stuff
from twisted.trial import unittest
import os

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Family.family import \
    FamilyModuleInformation

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_yaml = SetupPyHouseObj().BuildYaml(None)
        self.m_filename = 'families.yaml'

    def createFamilyObj(self):
        l_family_obj = FamilyModuleInformation()
        l_family_obj.Name = 'Insteon'
        l_family_obj.Key = 0
        l_family_obj.Active = True
        l_family_obj.FamilyPackageName = 'Modules.House.Family.Insteon'
        return l_family_obj


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_family')


class A1_Validate(SetupMixin, unittest.TestCase):
    """ This section tests the _test environment to be valid before testing the "Real" stuff.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Name(self):
        l_name = 'Insteon'
        print('Name: {}'.format(l_name))
        l_lc = l_name.lower()
        print('Name-lc: {}'.format(l_lc))
        l_cap = l_lc.capitalize()
        print('Name-cap: {}'.format(l_cap))


class A4_ValidFamily(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)

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
        SetupMixin.setUp(self)


class B2_One(SetupMixin, unittest.TestCase):
    """ This section tests the "lightingUtility" class
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_family_obj = familyUtil()._build_one_family_data(self.m_pyhouse_obj, 'Insteon')

    def test_01_BuildData(self):
        self.assertEqual(self.m_family_obj.Name, 'insteon')
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
        SetupMixin.setUp(self)
        self.m_family_obj = familyUtil()._build_one_family_data(self.m_pyhouse_obj, 'Insteon')

    def test_01_Import(self):
        l_obj = familyUtil()._init_family_component_apis(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'B3-01-A - Module'))
        self.assertNotEqual(l_obj, None)


class C1_Import(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        # self.m_family_obj = familyUtil()._build_one_family_data(self.m_pyhouse_obj, 'Insteon')

    def test_01_Import(self):
        l_family_obj = self.createFamilyObj()
        l_mod = 'Insteon_device'
        # print(PrettyFormatAny.form(l_family_obj, 'C1-01-A - Module'))
        # print(PrettyFormatAny.form(l_obj, 'C1-01-B - Module'))
        # self.assertNotEqual(l_obj, None)


class C2_Api(SetupMixin, unittest.TestCase):
    """ This section tests the creation of an Api reference
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_family_obj = familyUtil()._build_one_family_data(self.m_pyhouse_obj, 'Insteon')

    def test_01_Import(self):
        l_mod_name = 'insteon_device'
        l_mod_ref = None
        l_obj = familyUtil()._create_api_instance(self.m_pyhouse_obj, l_mod_name, l_mod_ref)
        print(PrettyFormatAny.form(l_obj, 'C2-01-A - Module'))
        self.assertNotEqual(l_obj, None)


class D1_One(SetupMixin, unittest.TestCase):
    """ This section tests the creation of one family Data
    """

    def setUp(self):
        SetupMixin.setUp(self)
        # self.m_family_obj = familyUtil()._build_one_family_data(self.m_pyhouse_obj, 'Insteon')

    def test_01_Null(self):
        l_mod_name = 'null'
        l_family_obj = familyUtil()._build_one_family_data(self.m_pyhouse_obj, l_mod_name)
        # print(PrettyFormatAny.form(l_family_obj, 'D1-01-A - Family'))
        self.assertEqual(l_family_obj.Name, l_mod_name)
        # self.assertNotEqual(l_obj, None)

    def test_02_Insteon(self):
        l_mod_name = 'insteon'
        l_family_obj = familyUtil()._build_one_family_data(self.m_pyhouse_obj, l_mod_name)
        # print(PrettyFormatAny.form(l_family_obj, 'D1-02-A - Family'))
        self.assertEqual(l_family_obj.Name, l_mod_name)

# ## END DBK
