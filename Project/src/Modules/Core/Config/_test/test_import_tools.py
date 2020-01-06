"""
@name:      Modules/Core/Config/_test/test_import_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Oct 24, 2019
@Summary:

Passed all 5 tests - DBK - 2019-11-04

"""

__updated__ = '2019-11-04'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.Config import import_tools

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

CONFIG_FILE_NAME = 'test.yaml'


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_yaml = SetupPyHouseObj().BuildYaml(None)

    def dump_to_file(self, p_yaml):
        """ For debugging to see a new _test.yaml file.
        Only do this once in the entire suite.  It overwrites any previous output.
        """
        self.m_yamlconf.write_yaml(p_yaml, self.m_filename, addnew=True)


class A0(unittest.TestCase):
    """ Identity
    """

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title')  # so it is defined when printing is cleaned up.
        print('Id: test_import_tools')


class I1_Import(SetupMixin, unittest.TestCase):
    """ Test the importing of modules
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_import = import_tools.Tools(self.m_pyhouse_obj)

    def test_00(self):
        print('I1-00')
        pass

    def test_01_Do_one(self):
        """
        """
        l_module = 'insteon_device'
        l_path = 'Modules.House.Family.Insteon'
        l_ret = self.m_import._do_import(l_module, l_path)
        # print(PrettyFormatAny.form(l_ret, 'I1-01-A - path'))
        self.assertIsNotNone(l_ret)

    def test_02_Do_several2(self):
        """
        """
        l_module = 'insteon_device'
        l_path = 'Modules.House.Family.Insteon'
        l_ret = self.m_import.import_module_get_api(l_module, l_path)
        # print(PrettyFormatAny.form(l_ret, 'I1-02-A - path'))
        self.assertIsNotNone(l_ret)

    def test_99(self):
        """
        """

# ## END DBK
