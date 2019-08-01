"""
@name:      PyHouse/src/Modules/Computer/Web/_test/test_web_mainpage.py
@author:    D Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 6, 2014
@Summary:

"""

__updated__ = '2019-03-01'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
# from Modules.Web import web_mainpage
from test.testing_mixin import SetupPyHouseObj
from Modules.Computer.Web.web_mainpage import modulepath, webpath
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_web_mainpage')


class B1_Path(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Modulepath(self):
        print(PrettyFormatAny.form(modulepath.path, 'B01-01-A - modulepath'))
        print(PrettyFormatAny.form(webpath.path, 'B01-01-A - modulepath'))
        self.assertEqual(modulepath.path, '/home/briank/workspace/PyHouse/Project/src/Modules/Computer/Web')

# ## END DBK
