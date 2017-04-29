"""
@name:      PyHouse/src/Modules.Core.Utilities.test/test_debug_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 8, 2015
@Summary:

Passed all 22 tests - DBK - 2017-04-23

"""
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

__updated__ = '2017-04-26'

#  Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

#  Import PyMh files
from Modules.Core.Utilities import debug_tools
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities.test.xml_xml_tools import XML_TEST, TESTING_TUPLE

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
    """Test FormatBytes functionality.
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
    """Testing _nuke newlines
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Short(self):
        """Testing _nuke_newlines().
        """
        l_max = 30
        l_short = 'This\nis\nshort.'
        l_ret = debug_tools._nuke_newlines(l_short)
        # print('B2-01-A Short: ', l_ret)
        self.assertLess(len(l_ret), l_max + 1)

    def test_02_Long(self):
        """Testing _nuke_newlines().
        """
        l_max = 50
        l_ret = debug_tools._nuke_newlines(LOTS_NLS)
        # print('B2-02-A Long: ', l_ret)
        self.assertLess(len(l_ret), l_max + 1)


class C1_Line(SetupMixin, unittest.TestCase):
    """Test _format_line
    Break a long line into one or more shorter lines based on maxlen.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Short_10(self):
        l_str = debug_tools._nuke_newlines(self.m_short)
        l_maxlen = 10
        l_ret = debug_tools._format_line(l_str, l_maxlen)
        print('C1-01-A Short Split: ', l_ret)
        self.assertEqual(len(l_ret), 2)

    def test_02_Short_50(self):
        l_str = debug_tools._nuke_newlines(self.m_short)
        l_maxlen = 50
        l_ret = debug_tools._format_line(l_str, l_maxlen)
        print('C1-02-A Short Whole: ', l_ret)
        self.assertEqual(len(l_ret), 1)

    def test_03_Long_10(self):
        l_str = debug_tools._nuke_newlines(self.m_long)
        l_maxlen = 10
        l_ret = debug_tools._format_line(l_str, l_maxlen)
        print('C1-02-A Short: ', l_ret)
        self.assertEqual(len(l_ret), 27)

    def test_04_Long_50(self):
        l_str = debug_tools._nuke_newlines(self.m_long)
        l_maxlen = 50
        l_ret = debug_tools._format_line(l_str, l_maxlen)
        print('C1-03-A Short: ', l_ret)
        self.assertEqual(len(l_ret), 9)


class C2_Cols(SetupMixin, unittest.TestCase):
    """Test format_cols functionality.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Short(self):
        """ Test formatting of columns
        """
        l_strings = ['1', '22', '333', '4444', '55555']
        l_widths = [10, 10, 10, 10, 10]
        l_ret = debug_tools._format_cols(l_strings, l_widths)
        print('\nC2-01-A - Cols:', l_ret)
        print(PrettyFormatAny.form(l_ret, "C2-01-B - Short Cols"))
        self.assertEqual(len(l_ret), 5 * 10 - (10 - 5))

    def test_02_Medium(self):
        """ Test formatting of columns
        """
        l_strings = ['1', 'now is the time', 'for all good men', 'to come to the aid', 'of their party']
        l_widths = [20, 20, 20, 20, 20]
        l_ret = debug_tools._format_cols(l_strings, l_widths)
        print('\nC2-02-A - Cols:', l_ret)
        print(PrettyFormatAny.form(l_ret, "C2-02-B - Medium Cols"))
        self.assertEqual(len(l_ret), 94)

    def test_03_Object(self):
        l_ret = debug_tools._formatObject('PyHouse', self.m_pyhouse_obj, maxlen=90, lindent=20)
        print('\nC2-03-A - Cols:', l_ret)
        print(PrettyFormatAny.form(l_ret, "C2-03-B - Object"))


class C3_Objs(SetupMixin, unittest.TestCase):
    """Test format_object functionality.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Cols(self):
        """ Test formatting of objs
        """
        l_ret = debug_tools._formatObject('PyHouse', self.m_pyhouse_obj, maxlen=120, lindent=20)
        print('\nC3-01-A - OBJS:', l_ret)



class D1_PFA(SetupMixin, unittest.TestCase):
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
        l_str = "The quick brown fox jumped over the lazy dog's back"  # 51 bytes
        l_len = len(l_str)
        l_ret = debug_tools.PrettyFormatAny._format_string(l_str, maxlen=40, indent=10)
        print('\nD1-01-A - String:\n' + l_ret)
        # self.assertEqual(len(l_str), l_len)
        # self.assertEqual(len(l_ret), 37)

    def test_02_unicode(self):
        l_ret = debug_tools.PrettyFormatAny._format_unicode(U_STRING, maxlen=40, indent=10)
        print('\nD1-02-A - Unicode:\n' + l_ret)
        pass

    def test_03_Dicts(self):
        l_ret = debug_tools.PrettyFormatAny._format_dict(DICTS, 50, 0)
        print('\nD1-03-A - Dicts:\n' + l_ret)
        self.assertEqual(len(l_ret), 177)

    def test_04_Xml(self):
        l_xml = ET.fromstring(XML_TEST)
        l_ret = debug_tools.PrettyFormatAny._format_XML(l_xml, maxlen=40, indent=10)
        print('\nD1-04-A - XML:\n' + l_ret)
        pass

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
