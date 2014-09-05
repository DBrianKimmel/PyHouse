"""
@name: PyHouse/src/Modules/utils/tools.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@note: Created on Apr 11, 2013
@license: MIT License
@summary: Various functions and utility methods.

"""


# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Core.data_objects import PyHouseData
from Modules.Core.setup_logging import LOGGING_DICT
from Modules.Utilities import tools
from Modules.Lighting import lighting_lights
from Modules.Families import family
from Modules.Computer import logging_pyh as Logger
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_01_Print(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_EMPTY))
        self.m_api = Logger.API()

    def test_0101_String(self):
        l_str = 'String A fairly long String that has no end, at least a fairly long one.'
        PrettyPrintAny(l_str, 'String')
        PrettyPrintAny(l_str, 'String', 10)

    def test_0102_Unicode(self):
        l_uc = u'A longish unicode string'
        PrettyPrintAny(l_uc, 'Unicode')
        PrettyPrintAny(l_uc, 'Unicode', 10)

    def test_0103_Dict(self):
        l_obj = LOGGING_DICT
        PrettyPrintAny(l_obj, 'Some Obj')

    def test_0104_XML(self):
        l_xml = self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        PrettyPrintAny(l_xml, 'XML')

    def test_0105_Obj(self):
        l_obj = self.m_pyhouse_obj
        PrettyPrintAny(l_obj, 'Obj')

    def test_0106_List(self):
        l_lst = [ 'AA', 1, {'a' : 1}, 'BB']
        PrettyPrintAny(l_lst, 'List')

    def test_0111_any(self):
        l_any = {'abc': 'Long A B C', 'def' : 'Another long thing.'}
        PrettyPrintAny(l_any)


class Test_02_Find(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_EMPTY))
        self.m_api = tools.GetPyhouse(self.m_pyhouse_obj)

    def test_0201_House(self):
        l_loc = self.m_api.Location().Latitude
        print(l_loc)

# ## END DBK
