"""
@name:      PyHouse/src/Modules/Utilities/test/test_json_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 25, 2015
@Summary:

Passed all 2 tests - DBK - 2015-08-07

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities import json_tools


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A01_Json(SetupMixin, unittest.TestCase):
    """
    This series tests the complex PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_Encode(self):
        l_json = json_tools.encode_json(self.m_pyhouse_obj)
        print(l_json)
        # PrettyFormatAny.form(l_json, "PyHouse_Obj")
        self.assertSubstring('Xml', l_json)
        self.assertSubstring('XmlOldVersion', l_json)

    def test_02_Decode(self):
        l_json = json_tools.encode_json(self.m_pyhouse_obj.Computer)
        l_dict = json_tools.decode_json_unicode(l_json)
        # print(debug_tools.PrettyFormatAny.form(l_dict, 'Decoded Inof'))
        self.assertEqual(l_dict['Name'], self.m_pyhouse_obj.Computer.Name)

# ## END DBK
