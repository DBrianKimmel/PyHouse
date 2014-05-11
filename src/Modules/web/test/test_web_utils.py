'''
Created on Jun 29, 2013

@author: briank
'''

from twisted.trial import unittest

from Modules.web import web_utils


PY_DATA = [ { 'a123': u'A', 'b': (2, 4), 'c': 3.0 }, 'def D E F' ]
JS_DATA = '{' + '}'


class Attribs(object):
    def_attr = 'Hello World!'

class Test(unittest.TestCase):

    def setUp(self):
        self.c_attr = Attribs()

    def tearDown(self):
        pass

    def test_001_encode(self):
        y = web_utils.MyJson().convert_to_unicode('abc')
        self.assertEquals(y, u'abc', "Convert to unicode failed.")

    def test_002_dencode(self):
        y = web_utils.MyJson().convert_from_unicode(u'ABC')
        self.assertEquals(y, 'ABC', "Convert from unicode failed.")

    def test_003_json_encode(self):
        x = PY_DATA
        y = web_utils.MyJson().encode_json(x)

    def test_004_json_decode(self):
        x = "{'de4' : 'D E F'}"
        y = web_utils.MyJson().decode_json(x)

    def Xtest_add_attrs(self):
        web_utils.add_attr_list(self.c_attr, ['abc/aaa', '/ddd/bbb.ext'])

# ## END DBK
