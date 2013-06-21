'''
Created on Apr 11, 2013

@author: briank
'''

import xml.etree.ElementTree as ET
from twisted.trial import unittest

from src.utils import xml_tools

XML = """
<Test b1='True' f1='3.14158265' i1='371' t1='Test of text' >
    <BoolField>True</BoolField>
    <FloatField>3.14158265</FloatField>
    <IntField>371</IntField>
    <TextField>Test of text</TextField>
    <Part_3 b3='True' f3='3.14158265' i3='371' t3='Test of text' />
</Test>
"""

class Test(unittest.TestCase):

    def _get_xml(self):
        l_xml = ET.fromstring(XML)
        return l_xml

    def setUp(self):
        # self.api = xml_tools.ConfigTools()
        self.api = xml_tools.PutGetXML()

    def tearDown(self):
        pass

    def test_000(self):
        xml_tools.prettify(self._get_xml())

    def test_001_get_bool(self):
        result = self.api.get_bool_from_xml(self._get_xml(), 'BoolField')
        self.assertTrue(result)
        result = self.api.get_bool_from_xml(self._get_xml(), 'b1')
        self.assertTrue(result)
        result = self.api.get_bool_from_xml(self._get_xml(), 'Part_3/b3')
        self.assertTrue(result)

    def test_002_get_int(self):
        result = self.api.get_int_from_xml(self._get_xml(), 'IntField')
        self.assertEqual(result, 371)
        result = self.api.get_int_from_xml(self._get_xml(), 'i1')
        self.assertEqual(result, 371)

    def test_003_get_text(self):
        l_xml = self._get_xml()
        result = self.api.get_text_from_xml(l_xml, 'TextField')
        self.assertEqual(result, 'Test of text')
        result = self.api.get_text_from_xml(l_xml, 't1')
        self.assertEqual(result, 'Test of text')

    def test_004_get_float(self):
        l_xml = self._get_xml()
        result = self.api.get_float_from_xml(l_xml, 'FloatField')
        self.assertAlmostEqual(result, float(3.1415825435), places = 5, msg = 'get_float_from_xml failed')
        result = self.api.get_float_from_xml(l_xml, 'f1')
        self.assertAlmostEqual(result, float(3.1415825435), places = 5, msg = 'get_float_from_xml failed')

# ## END
