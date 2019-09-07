"""
@name:      /home/briank/workspace/Pyhouse/src/Modules/Housing/Rules/_test/test_rules_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Feb 1, 2017
@summary:   Test

"""

__updated__ = '2018-02-13'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Housing.Rules.rules_xml import Xml as rulesXml
from Modules.Housing.test.xml_housing import \
    TESTING_HOUSE_DIVISION
from Modules.Housing.Rules.test.xml_rules import \
    TESTING_RULES_SECTION, \
    TESTING_RULE, \
    TESTING_RULE_NAME_0, \
    TESTING_RULE_ACTIVE_0, \
    TESTING_RULE_KEY_0, \
    TESTING_RULE_UUID_0, XML_RULES_SECTION
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_rules')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the above setup for things we will need further down in the tests.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Tags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)
        self.assertEqual(self.m_xml.rules_sect.tag, TESTING_RULES_SECTION)
        self.assertEqual(self.m_xml.rule.tag, TESTING_RULE)


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))

    def test_01_Raw(self):
        l_raw = XML_RULES_SECTION
        # print(l_raw)
        self.assertEqual(l_raw[:14], '<RulesSection>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_RULES_SECTION)
        # print(PrettyFormatAny.form(l_xml, 'A2-02-A -Xml'))
        self.assertEqual(l_xml.tag, TESTING_RULES_SECTION)


class B1_Read(SetupMixin, unittest.TestCase):
    """ Test Reading of XML
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_rules(self):
        l_xml = self.m_xml.rules_sect[0]
        l_obj = rulesXml.read_rules_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'A2-03-A - House'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_RULE_NAME_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_RULE_ACTIVE_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_RULE_KEY_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_RULE_UUID_0)

# ## END DBK
