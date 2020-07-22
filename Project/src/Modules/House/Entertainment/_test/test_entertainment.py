"""
@name:      Modules/House/Entertainment/_test/test_entertainment.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 14, 2013
@summary:   Test

Passed all 6 tests - DBK - 2030-01-27

"""

__updated__ = '2020-01-27'

# Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

# Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Entertainment.entertainment import Api as entertainmentApi
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

TEST_YAML = """\
Entertainment:
    Services:
        - Pandora: !include pandora.yaml
    Devices:
        - Onkyo: !include onkyo.yaml
        - Samsung: !include samsung.yaml
"""


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        l_yaml = YAML()
        self.m_test_config = l_yaml.load(TEST_YAML)
        self.m_api = entertainmentApi(self.m_pyhouse_obj)


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_entertainment')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Pyhouse(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        self.assertIsNotNone(self.m_pyhouse_obj)

    def test_02_House(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A1-02-A - House'))
        self.assertIsNotNone(self.m_pyhouse_obj.House)

    def test_03_Entertainment(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'A1-03-A - Entertainment'))
        self.assertIsNotNone(self.m_pyhouse_obj.House.Entertainment)


class C1_Load(SetupMixin, unittest.TestCase):
    """ This will _test all of the sub modules ability to load their part of the XML file
            and this modules ability to put everything together in the structure
    """

    def setUp(self):
        SetupMixin.setUp(self)


class D1_Save(SetupMixin, unittest.TestCase):
    """ Test writing of the entertainment XML.
    """

    def setUp(self):
        SetupMixin.setUp(self)

# ## END DBK
