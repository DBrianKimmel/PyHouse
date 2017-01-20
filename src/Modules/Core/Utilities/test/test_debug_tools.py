"""
@name:      PyHouse/src/Modules.Core.Utilities.test/test_debug_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 8, 2015
@Summary:

Passed all 9 tests - DBK - 2016-11-22

"""

__updated__ = '2017-01-19'

#  Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

#  Import PyMh files
from Modules.Core.Utilities import debug_tools
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj

STRING = 'Now is the time for all good men to come to the aid of something or other.'
LISTS = [1, 2, 3, [4, 5, 6], 7, [8, 9, [10, 11], 12]]
DICTS = {   'a' : '1',
            'b' : '2',
            'c' : {   'd' : '3',
                'e' : 'hello' },
            'f' : 55
         }
LOTS_NLS = 'now\r' + 'is\n' + 'the\n\r' + 'time\r\n' + 'for\n' + 'all\n' \
            'good\n' + 'men\n' + 'to\n' + 'leave.\n'


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_debug_tools')


class B1_X(SetupMixin, unittest.TestCase):
    """Test PrintBytes functionality.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_long = "In order for your computers to be useful, they must be set up on a network.\n" \
                        "That network could be a private network, a private network connected to the internet or the public internet itself. " \
                        " With IPv4 (addresses like 123.45.67.89) you almost always have to have a private network, connected to the internet or not.  " \
                        "With new IPv6 (addresses like 2001:db8::dead:beef) you will probably have an address on the public internet."

    def test_01_Line(self):
        """Testing _nuke_newlines().
        """
        l_ret = debug_tools._nuke_newlines(LOTS_NLS)
        # print('B1-01-A Line', l_ret)
        self.assertEqual(len(l_ret), 43)


class B2_Format(SetupMixin, unittest.TestCase):
    """Test PrintBytes functionality.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_long = "In order for your computers to be useful, they must be set up on a network.\n" \
                        "That network could be a private network, a private network connected to the internet or the public internet itself. " \
                        " With IPv4 (addresses like 123.45.67.89) you almost always have to have a private network, connected to the internet or not.  " \
                        "With new IPv6 (addresses like 2001:db8::dead:beef) you will probably have an address on the public internet."

    def test_01_Line(self):
        """Testing _format_line().
        """
        l_ret = debug_tools._format_line(self.m_long, maxlen=40)
        # print('B2-01-A - Line', l_ret)
        self.assertEqual(len(l_ret), 12)

    def test_02_Newlines(self):
        """Teting _nuke_newlines().
        """
        l_ret = debug_tools._nuke_newlines(self.m_long)
        # print('B2_02-A - NewLine', l_ret)
        self.assertEqual(len(l_ret), 426)

    def test_03_Cols(self):
        l_strings = ['1', '22', '333', '4444']
        l_widths = [10, 10, 10, 10]
        l_ret_1 = debug_tools._format_cols(l_strings, l_widths)
        # print('B2-03-A - Cols', l_ret_1)
        self.assertEqual(len(l_ret_1), 40 - (10 - 4))
        l_strings = ['1', 'now is the time for all good men', 'to come to the aid', 'of their party']
        l_ret_2 = debug_tools._format_cols(l_strings, l_widths)
        # print(l_ret_2)

    def test_04_Object(self):
        l_ret = debug_tools._format_object('PyHouse', self.m_pyhouse_obj, maxlen=120, lindent=20)
        # print(l_ret)


class B3_PFA(SetupMixin, unittest.TestCase):
    """
    PrettyFormatAll
    """
    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_String(self):
        l_str = "The quick brown fox jumpped over the lazy dog's back"
        l_len = len(l_str)
        l_ret = debug_tools.PrettyFormatAny._format_string(l_str, maxlen=40, indent=10)
        # print(l_ret)
        self.assertEqual(len(l_str), l_len)
        self.assertEqual(len(l_ret), l_len + 20 + 1)

    def test_02_Lists(self):
        l_ret = debug_tools.PrettyFormatAny._format_list(LISTS, 50, 0)
        # print(l_ret)

    def test_03_Dicts(self):
        l_ret = debug_tools.PrettyFormatAny._format_dict(DICTS, 50, 0)
        # print(l_ret)

#  ## END DBK
