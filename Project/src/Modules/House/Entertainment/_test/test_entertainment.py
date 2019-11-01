"""
@name:      Modules/House/Entertainment/_test/test_entertainment.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 14, 2013
@summary:   Test

Passed all 13 tests - DBK - 2019-03-18

"""

__updated__ = '2019-10-29'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Entertainment.entertainment import Api as entertainmentApi
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
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

    def test_1_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Tags'))
        self.assertEqual(self.m_pyhouse_obj.House.Rooms, {})


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
