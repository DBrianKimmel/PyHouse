"""
@name:      PyHouse/Project/src/Modules/Core/Utilities/_test/test_extract_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Oct 4, 2018
@summary:   Test

Passed all 1 tests - DBK - 2018-08-02

"""

__updated__ = '2018-10-05'

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities import extract_tools
from Modules.Core.Utilities.extract_tools import extract_quoted

P1 = b'  "Carroll County Blues" by "Bryan Sutton" on "Not Too Far From The Tree" @ Bluegrass Radio'
P2 = b'   "Love Is On The Way" by "Dave Koz" on "Greatest Hits" <3 @ Smooth Jazz Radio'


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_debug_tools')


class B1_Quoted(SetupMixin, unittest.TestCase):
    """Test FormatBytes functionality.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Short(self):
        """Testing _nuke_newlines().
        """
        l_x = 'a'
        l_first, l_rest = extract_quoted(P1)
        print('B1-01-A - P1 - Str:{};  Rest:{}'.format(l_first, l_rest))

    def test_02_Short(self):
        """Testing _nuke_newlines().
        """
        l_x = 'a'
        l_first, l_rest = extract_quoted(P1, b'"')
        print('B1-02-A - P1 - Str:{};  Rest:{}'.format(l_first, l_rest))

    def test_03_Short(self):
        """Testing _nuke_newlines().
        """
        l_x = 'a'
        l_ret, bb = extract_quoted(P2)
        print('B1-01-A P1: ', l_ret, bb)

    def test_04_Short(self):
        """Testing _nuke_newlines().
        """
        l_x = 'a'
        l_ret = extract_quoted(P2, b'"')
        print('B1-01-A P1: ', l_ret)

# ## END DBK
