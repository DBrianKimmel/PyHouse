"""
@name: PyHouse/src/Modules/test/test_communication.py
@author: d. Brian Kimmel
@contact: <d.briankimmel@gmail.com>
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Aug 16, 2014
@Summary:

"""

# Import system type stuff
from twisted.trial import unittest, runner

# Import PyMh files and modules.


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Communication(self):
        from Modules.communication import test
        test()
        print('Ran Modules.test.communication')

# ## END DBK
