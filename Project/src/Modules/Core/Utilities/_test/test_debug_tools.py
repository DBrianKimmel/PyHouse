"""
@name:      Modules/Core/Utilities/_test/test_debug_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 8, 2015
@Summary:

Passed all 22 tests - DBK - 2018-08-02

"""

__updated__ = '2019-08-10'

#  Import system type stuff
from twisted.trial import unittest

#  Import PyMh files
from Modules.Core.Utilities import debug_tools
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.Utilities._test.xml_xml_tools import TESTING_TUPLE

STRING = 'Now is the time for all good men to come to the aid of something or other.'
U_STRING = u'Now is NOT the time for any bad women to go to the aid of nothing not evil.'
LISTS = [1, 2, 3, [4, 5, 6], 7, [8, 9, [10, 11], 12]]
DICTS = {   'a' : '1',
            'b' : '2',
            'c' : {   'd' : '3',
                'e' : 'hello' },
            'f' : 55
         }
LOTS_NLS = 'Now\r' + '   is\n' + 'the\n\r' + 'time\r\n' + 'for\n' + 'all\n' \
            'good\n' + 'men\n' + 'to\n' + 'leave.\n'


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_long = "In order for your computers to be useful, they must be set up on a network.\n" \
                        "That network could be a private network, a private network connected to the internet or the public internet itself. " \
                        " With IPv4 (addresses like 123.45.67.89) you almost always have to have a private network, connected to the internet or not.  " \
                        "With new IPv6 (addresses like 2001:db8::dead:beef) you will probably have an address on the public internet."
        self.m_short = "This is short"
        self.m_empty = ''


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_debug_tools')


class B1_Truncate(SetupMixin, unittest.TestCase):
    """Test FormatBytes functionality.
    """

    def setUp(self):
        SetupMixin.setUp(self)

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

    def test_03_Empty(self):
        """Testing _nuke_newlines().
        """
        l_max = 40
        l_ret = debug_tools._trunc_string(self.m_empty, l_max)
        # print('B1-03-A Empty:>>{}<<'.format(l_ret))
        self.assertLess(len(l_ret), l_max + 1)


class B2_Newlines(SetupMixin, unittest.TestCase):
    """Testing _nuke newlines
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Short(self):
        """Testing _nuke_newlines().
        """
        l_max = 30
        l_short = 'This\nis\nshort.'
        l_ret = debug_tools._nuke_newlines(l_short)
        # print('B2-01-A Short: ', l_ret)
        # print('-----')
        self.assertLess(len(l_ret), l_max + 1)

    def test_02_Long(self):
        """Testing _nuke_newlines().
        """
        l_max = 50
        l_ret = debug_tools._nuke_newlines(LOTS_NLS)
        # print('B2-02-A Long: ', l_ret)
        # print('-----')
        self.assertLess(len(l_ret), l_max + 1)

    def test_03_Empty_1(self):
        """Testing _nuke_newlines().
        """
        l_max = 30
        l_short = 'This\n\n\n\n'
        l_ret = debug_tools._nuke_newlines(l_short)
        print('B2-03-A Empty_1:>>{}<<'.format(l_ret))
        self.assertLess(len(l_ret), l_max + 1)


class C1_Line(SetupMixin, unittest.TestCase):
    """Test _format_line
    Break a long line into one or more shorter lines based on maxlen.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Short_10(self):
        l_str = debug_tools._nuke_newlines(self.m_short)
        l_maxlen = 10
        l_ret = debug_tools._format_line(l_str, l_maxlen)
        # print('\nC1-01-A Short Split: ', l_ret)
        self.assertEqual(len(l_ret), 2)

    def test_02_Short_50(self):
        l_str = debug_tools._nuke_newlines(self.m_short)
        l_maxlen = 50
        l_ret = debug_tools._format_line(l_str, l_maxlen)
        # print('\nC1-02-A - Short 50: ', l_ret)
        self.assertEqual(len(l_ret), int((len(l_str) + l_maxlen - 1) / l_maxlen))

    def test_03_Long_10(self):
        l_str = debug_tools._nuke_newlines(self.m_long)
        l_maxlen = 10
        l_ret = debug_tools._format_line(l_str, l_maxlen)
        print('\nC1-03-A Long 10: ', l_ret)
        self.assertEqual(len(l_ret), 27)

    def test_04_Long_50(self):
        l_str = debug_tools._nuke_newlines(self.m_long)
        l_maxlen = 50
        l_ret = debug_tools._format_line(l_str, l_maxlen)
        # print('\nC1-04-A Long 50: ', l_ret)
        self.assertEqual(len(l_ret), 9)

    def test_05_xx(self):
        l_str = 'Comment\n'
        l_str = debug_tools._nuke_newlines(l_str)
        l_maxlen = 50
        l_ret = debug_tools._format_line(l_str, l_maxlen)
        print('\nC1-05-A Long 50: ', l_ret)
        self.assertEqual(len(l_ret), 1)


class C2_Cols(SetupMixin, unittest.TestCase):
    """Test format_cols functionality.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Short(self):
        """ Test formatting of columns
        """
        l_strings = ['1', '22', '333', '4444', '55555']
        l_widths = [10, 10, 10, 10, 10]
        l_ret = debug_tools._format_cols(l_strings, l_widths)
        # print('\nC2-01-A - Cols:', l_ret)
        # print(PrettyFormatAny.form(l_ret, "C2-01-B - Short Cols"))
        self.assertEqual(len(l_ret), 5 * 10 - (10 - 5))

    def test_02_Medium(self):
        """ Test formatting of columns
        """
        l_strings = ['1', 'now is the time', 'for all good men', 'to come to the aid', 'of their party']
        l_widths = [20, 20, 20, 20, 20]
        l_ret = debug_tools._format_cols(l_strings, l_widths)
        # print('\nC2-02-A - Cols:', l_ret)
        # print(PrettyFormatAny.form(l_ret, "C2-02-B - Medium Cols"))
        self.assertEqual(len(l_ret), 94)

    def test_03_Object(self):
        l_ret = debug_tools._formatObject('PyHouse', self.m_pyhouse_obj, maxlen=90, lindent=20)
        print('\nC2-03-A - Object:', l_ret)
        print(PrettyFormatAny.form(l_ret, "C2-03-B - Object"))
        l_ret = PrettyFormatAny.form(self.m_pyhouse_obj, 'XXX')

        # print(PrettyFormatAny.form(self.m_pyhouse_obj, "C2-03-C - Object"))
        # self.assertEqual(len(l_ret), 984)

    def test_04_Empty(self):
        """ Test formatting of columns
        """
        l_strings = ['Comment', ' ']
        l_widths = [10, 10]
        l_ret = debug_tools._format_cols(l_strings, l_widths)
        print('\nC2-04-A - Cols:', l_ret)
        print(PrettyFormatAny.form(l_ret, "C2-04-B - Empty Cols"))
        self.assertEqual(len(l_ret), 2 * 10 - (10 - 5))

    def test_05_Empty(self):
        """ Test formatting of columns
        """
        l_strings = ['Comment', ' ']
        l_widths = [10, 10]

        l_lines = list(map(debug_tools._nuke_newlines, l_strings))
        print('\nC2-05-A - Lines:', l_lines)


class C3_Objs(SetupMixin, unittest.TestCase):
    """Test format_object functionality.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Cols(self):
        """ Test formatting of objs
        """
        l_ret = debug_tools._formatObject('PyHouse', self.m_pyhouse_obj, maxlen=120, lindent=20)
        print('\nC3-01-A - OBJS:', l_ret)
        # self.assertEqual(len(l_ret), 1128)


class D1_PFA(SetupMixin, unittest.TestCase):
    """
    PrettyFormatAll
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_String(self):
        """ Test formatting of string literals

        should produce:

        The quick brown fox jumped
        over the lazy dog's back
        """
        l_str = "The quick brown fox jumped over the lazy dog's back"  # 51 bytes
        # l_len = len(l_str)
        l_ret = debug_tools.PrettyFormatAny._format_string(l_str, maxlen=40, indent=10)
        print('\nD1-01-A - String:\n' + l_ret)
        self.assertLessEqual(len(l_str), 51)
        # self.assertEqual(len(l_ret), 37)

    def test_02_unicode(self):
        l_ret = debug_tools.PrettyFormatAny._format_unicode(U_STRING, maxlen=40, indent=10)
        print('\nD1-02-A - Unicode:\n' + l_ret)
        pass

    def test_03_Dicts(self):
        l_ret = debug_tools.PrettyFormatAny._format_dict(DICTS, 50, 0)
        print('\nD1-03-A - Dicts:\n' + l_ret)
        self.assertGreaterEqual(len(l_ret), 1)

    def test_05_Lists(self):
        l_ret = debug_tools.PrettyFormatAny._format_list(LISTS, 50, 0)
        print('\nD1-05-A - Lists:\n' + l_ret)
        self.assertEqual(len(l_ret), 87)

    def test_06_Tuple(self):
        l_ret = debug_tools.PrettyFormatAny._format_tuple(TESTING_TUPLE, maxlen=40, indent=10)
        print('\nD1-06-A - Tuple:\n' + l_ret)
        pass

    def test_07_Obj(self):
        l_ret = debug_tools.PrettyFormatAny._format_object(self.m_pyhouse_obj, maxlen=40, indent=10)
        print('\nD1-07-A - Object:\n' + l_ret)
        pass

    def test_08_None(self):
        l_ret = debug_tools.PrettyFormatAny._format_none(None)
        print('\nD1-08-A - None:\n' + l_ret)
        pass

    def test_09_ByteArray(self):
        l_ret = debug_tools.PrettyFormatAny._format_bytearray(b'\01\02\03', maxlen=40, indent=10)
        print('\nD1-09-A - ByteArray:\n' + l_ret)
        pass

#  ## END DBK