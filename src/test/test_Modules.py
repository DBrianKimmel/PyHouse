"""
@name:      PyHouse/src/test/test_Modules.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 16, 2014
@Summary:

"""
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testModules(self):
        from Modules import test
        print('Ran Modules.test')

# ## END DBK
