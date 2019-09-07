"""
-*- _test-case-name: Pyhouse/src/Modules/Computer/Web/_test/test_web_nodes.py -*-

@name:      Pyhouse/src/Modules/Computer/Web/_test/test_web_nodes.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2017 by D. Brian Kimmel
@note:      Created on Jan 9, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2017-01-11'


# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
# from Modules.Web import web_mainpage
from test import xml_data
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_web_nodes')


# ## END DBK
