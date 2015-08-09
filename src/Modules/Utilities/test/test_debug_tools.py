"""
@name:      PyHouse/src/Modules/Utilities/test/test_debug_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 8, 2015
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Utilities import debug_tools
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj

STRING = 'Now is the time for all good men to come to the aid of something or other.'

class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A_Format(SetupMixin, unittest.TestCase):
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
        l_ret = debug_tools._format_line(self.m_long, maxlen = 40)
        print(l_ret)
        self.assertEqual(len(l_ret), 12)

    def test_02_Newlines(self):
        """Teting _nuke_newlines().
        """
        l_ret = debug_tools._nuke_newlines(self.m_long)
        print(l_ret)
        self.assertEqual(len(l_ret), 426)

    def test_03_Cols(self):
        l_strings = ['1', '22', '333', '4444']
        l_widths = [10, 10, 10, 10]
        l_ret_1 = debug_tools._format_cols(l_strings, l_widths)
        print(l_ret_1)
        self.assertEqual(len(l_ret_1), 40 - (10 - 4))
        l_strings = ['1', 'now is the time for all good men', 'to come to the aid', 'of their party']
        l_ret_2 = debug_tools._format_cols(l_strings, l_widths)
        print(l_ret_2)

    def test_04_Object(self):
        l_ret = debug_tools._format_object('PyHouse', self.m_pyhouse_obj, maxlen = 120, lindent = 20)
        print(l_ret)


# ## END DBK
