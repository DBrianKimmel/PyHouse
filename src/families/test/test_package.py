'''
Created on Apr 9, 2013

@author: briank
'''

import inspect
import os
from twisted.trial import unittest

from families.__init__ import VALID_FAMILIES


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_valid_families(self):
        path_inspect = inspect.getfile(inspect.currentframe()) # script filename (usually with path)
        path_file = os.path.abspath(__file__)
        l_dir = os.path.dirname(path_file)
        l_dir = os.path.dirname(l_dir)
        l_dir_list = os.listdir(l_dir)
        for l_name in VALID_FAMILIES:
            self.assertTrue(l_name in l_dir_list)
            print "found ", l_name
        #print l_dir_list
        #families = os.dirs

### END
