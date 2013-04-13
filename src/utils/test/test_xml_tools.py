'''
Created on Apr 11, 2013

@author: briank
'''

import xml.etree.ElementTree as ET
from twisted.trial import unittest

from utils import xml_tools

XML = """
<Test>
    <BoolField>True</BoolField>
    <FloatField>3.14158265</FloatField>
    <IntField>371</IntField>
    <TextField>Test of text</TextField>
</Test>
"""

class Test(unittest.TestCase):

    def _get_xml(self):
        l_xml = ET.fromstring(XML)
        return l_xml

    def setUp(self):
        self.api = xml_tools.ConfigTools()

    def tearDown(self):
        pass

    def test_001_get_boolt(self):
        result = self.api.get_int_element(self._get_xml(), 'BoolField')
        self.assertTrue(result)

    def test_002_get_int(self):
        result = self.api.get_int_element(self._get_xml(), 'IntField')
        self.assertEqual(result, 371)

    def test_get_text_element(self):
        l_xml = self._get_xml()
        result = self.api.get_text_element(l_xml, 'TextField')
        self.assertEqual(result, 'Text of text')

    def testfloat(self):
        l_xml = self._get_xml()
        result = self.api.get_float_element(l_xml, 'FloatField')
        self.assertAlmostEqual(result, float(3.1415825435), places = 5, msg = 'get_float_element failed')

### END
