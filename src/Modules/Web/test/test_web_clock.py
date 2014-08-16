"""
@name: PyHouse/src/Modules/web/test/test_web_clock.py
@author: briank
@contact: <d.briankimmel@gmail.com>
@Copyright: (c)  2014 by briank
@license: MIT License
@note: Created on Jun 21, 2014
@Summary:

"""

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
# from Modules.utils.tools import PrettyPrintAny
from src.test import test_mixin


class SetupMixin(object):
    """
    """

    def setUp(self):
        test_mixin.Setup()
        # self.m_api = schedule.API()


class Test(SetupMixin, unittest.TestCase):

    def setUp(self):
        self.m_root_xml = None
        SetupMixin.setUp(self)
        pass

    def testName(self):
        pass

# ## END DBK
