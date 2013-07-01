'''
Created on Jun 29, 2013

@author: briank
'''

from twisted.trial import unittest

from src.web import web_utils

class Attribs(object):
    def_attr = 'Hello World!'

class Test(unittest.TestCase):

    def setUp(self):
        self.c_attr = Attribs()

    def tearDown(self):
        pass

    def testName(self):
        pass

    def test_add_attrs(self):
        web_utils.add_attr_list(self.c_attr, ['abc/aaa', '/ddd/bbb.ext'])
        print "vars =", vars(self.c_attr)
        print "dict =", self.c_attr.__dict__

# ## END DBK
