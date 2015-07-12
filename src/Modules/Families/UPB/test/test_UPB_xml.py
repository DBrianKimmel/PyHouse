"""
@name:      PyHouse/src/Modules/Families/UPB/test/test_UPB_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2015 by briank
@license:   MIT License
@note:       Created on Aug 6, 2014
@Summary:

"""

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
# from Modules.Families.UPB import UPB_xml
from test.testing_mixin import SetupPyHouseObj
# from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_01_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testName(self):
        pass

# ## END DBK
