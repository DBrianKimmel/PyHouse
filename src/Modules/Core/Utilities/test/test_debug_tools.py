"""
@name:      PyHouse/src/Modules.Core.Utilities.test/test_debug_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 8, 2015
@Summary:

Passed all 12 tests - DBK - 2017-04-01

"""

__updated__ = '2017-04-01'

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
        self.m_long = "In order for your computers to be useful, they must be set up on a network.\n" \
                        "That network could be a private network, a private network connected to the internet or the public internet itself. " \
                        " With IPv4 (addresses like 123.45.67.89) you almost always have to have a private network, connected to the internet or not.  " \
                        "With new IPv6 (addresses like 2001:db8::dead:beef) you will probably have an address on the public internet."
        self.m_short = "This is short"


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_debug_tools')


class B1_Truncate(SetupMixin, unittest.TestCase):
    """Test PrintBytes functionality.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Short(self):
        """Testing _nuke_newlines().
        """
        l_max = 30
        l_ret = debug_tools._trunc_string(self.m_short, l_max)
        # print('B1-01-A Short: ', l_ret)
        self.assertLess(len(l_ret), l_max + 1)

    def test_02_Long(self):
        """Testing _nuke_newlines().
        """
        l_max = 40
        l_ret = debug_tools._trunc_string(self.m_long, l_max)
        # print('B1-02-A Long: ', l_ret)
        self.assertLess(len(l_ret), l_max + 1)


class B2_Newlines(SetupMixin, unittest.TestCase):
    """Test
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Short(self):
        """Testing _nuke_newlines().
        """
        l_max = 30
        l_short = 'This\nis\nshort.'
        l_ret = debug_tools._nuke_newlines(l_short)
        print('B2-01-A Short: ', l_ret)
        self.assertLess(len(l_ret), l_max + 1)


class C1_Line(SetupMixin, unittest.TestCase):
    """Test
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Short(self):
        l_str = debug_tools._nuke_newlines(self.m_short)
        l_strlen = 1
        #
        l_maxlen = 10
        l_short_ret = debug_tools._format_line(l_str, l_maxlen)
        # print('B3-01-A Short Split: ', l_short_ret)
        #
        l_maxlen = 50
        l_long_ret = debug_tools._format_line(l_str, l_maxlen)
        # print('B3-01-B Short Whole: ', l_long_ret)
        #
        self.assertEqual(len(l_short_ret), 2)
        self.assertEqual(len(l_long_ret), 1)

    def test_02_Long(self):
        l_str = debug_tools._nuke_newlines(self.m_long)
        #
        l_maxlen = 10
        l_short_ret = debug_tools._format_line(l_str, l_maxlen)
        print('B3-01-A Short: ', l_short_ret)
        #
        l_maxlen = 50
        l_long_ret = debug_tools._format_line(l_str, l_maxlen)
        print('B3-01-B Short: ', l_long_ret)
        # self.assertEqual(len(list(l_str)), len(l_short_ret))
        self.assertEqual(len(l_short_ret), 9)
        self.assertEqual(len(l_long_ret), 1)


class C2_Cols(SetupMixin, unittest.TestCase):
    """Test PrintBytes functionality.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Cols(self):
        """ Test formatting of columns
        """
        l_strings = ['1', '22', '333', '4444']
        l_widths = [10, 10, 10, 10]
        l_ret_1 = debug_tools._format_cols(l_strings, l_widths)
        # print('B2-03-A - Cols', l_ret_1)
        self.assertEqual(len(l_ret_1), 40 - (10 - 4))
        l_strings = ['1', 'now is the time for all good men', 'to come to the aid', 'of their party']
        l_ret_2 = debug_tools._format_cols(l_strings, l_widths)
        # print(l_ret_2)

    def test_02_Object(self):
        l_ret = debug_tools._format_object('PyHouse', self.m_pyhouse_obj, maxlen=120, lindent=20)
        # print(l_ret)


class C3_Objs(SetupMixin, unittest.TestCase):
    """Test PrintBytes functionality.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Cols(self):
        """ Test formatting of columns
        """
        l_ret = debug_tools._format_object('PyHouse', self.m_pyhouse_obj, maxlen=120, lindent=20)
        print(l_ret)



class D3_PFA(SetupMixin, unittest.TestCase):
    """
    PrettyFormatAll
    """
    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_String(self):
        """ Test formatting of string literals

        should produce:

        The quick brown fox jumped
        over the lazy dog's back
        """
        l_str = "The quick brown fox jumped over the lazy dog's back"
        l_len = len(l_str)
        l_ret = debug_tools.PrettyFormatAny._format_string(l_str, maxlen=40, indent=10)
        print(l_ret)
        self.assertEqual(len(l_str), len(l_ret))
        self.assertEqual(len(l_ret), l_len + 20 + 1)

    def test_02_Lists(self):
        l_ret = debug_tools.PrettyFormatAny._format_list(LISTS, 50, 0)
        # print(l_ret)

    def test_03_Dicts(self):
        l_ret = debug_tools.PrettyFormatAny._format_dict(DICTS, 50, 0)
        # print(l_ret)

#  ## END DBK
