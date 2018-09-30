"""
-*- test-case-name: /home/briank/workspace/PyHouse/src/Modules/Computer/Bridges/test/test_bridges.py -*-

@name:      /home/briank/workspace/PyHouse/src/Modules/Computer/Bridges/test/test_bridges.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@note:      Created on Dec 23, 2017
@license:   MIT License
@summary:

Passed all 6 tests - DBK - 2018-02-12

"""

__updated__ = '2018-02-12'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Computer.Bridges.bridges import API as bridgesAPI
from Modules.Computer.test.xml_computer import TESTING_COMPUTER_DIVISION
from Modules.Core.Utilities import json_tools
from Modules.Computer.Bridges.test.xml_bridges import \
        XML_BRIDGES, \
        TESTING_BRIDGES_SECTION, \
        TESTING_BRIDGE_NAME_0, \
        TESTING_BRIDGE_NAME_1, \
        TESTING_BRIDGE_COMMENT_0
# from Modules.Core.Utilities.debug_tools import FormatBytes
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)

    def jsonPair(self, p_json, p_key):
        """ Extract key, value from json
        """
        l_json = json_tools.decode_json_unicode(p_json)
        try:
            l_val = l_json[p_key]
        except (KeyError, ValueError) as e_err:
            l_val = 'ERRor on JsonPair for key "{}"  {} {}'.format(p_key, e_err, l_json)
            print(l_val)
        return l_val


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_bridges')


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.Computer.Mqtt.Prefix = "pyhouse/test_house/"

    def test_01_Tags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, TESTING_COMPUTER_DIVISION)


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_BRIDGES
        # print('A2-01-A - Raw', l_raw)
        self.assertEqual(l_raw[:16], '<BridgesSection>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_BRIDGES)
        # print('A2-02-A - Parsed', l_xml)
        self.assertEqual(l_xml.tag, TESTING_BRIDGES_SECTION)


class B1_API(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.Computer.Mqtt.Prefix = "pyhouse/test_house/"

    def test_01_Load(self):
        """ Be sure that the XML contains the right stuff.
        """
        bridgesAPI(self.m_pyhouse_obj).LoadXml(self.m_pyhouse_obj)
        l_bridges = self.m_pyhouse_obj.Computer.Bridges
        # print(PrettyFormatAny.form(l_bridges, 'B1-01-A - Load'))
        self.assertEqual(l_bridges[0].Name, TESTING_BRIDGE_NAME_0)
        self.assertEqual(l_bridges[1].Name, TESTING_BRIDGE_NAME_1)

    def test_02_Save(self):
        """
        """
        l_xml = ET.Element('PyHouse')
        bridgesAPI(self.m_pyhouse_obj).LoadXml(self.m_pyhouse_obj)
        l_bridges = self.m_pyhouse_obj.Computer.Bridges
        # print(PrettyFormatAny.form(l_bridges, 'B1-02-A - Load'))
        l_out = bridgesAPI(self.m_pyhouse_obj).SaveXml(l_xml)
        # print(PrettyFormatAny.form(l_out, 'B1-02-B - XML'))
        l_out = l_out.find('Bridge')
        # print(PrettyFormatAny.form(l_out, 'B1-02-C - Bridges'))
        self.assertEqual(l_out.find('Comment').text, TESTING_BRIDGE_COMMENT_0)

# ## END DBK
