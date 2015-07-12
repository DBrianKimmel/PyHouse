"""
@name:      PyHouse/src/Modules/Utilities/test_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2013-2015 by D. Brian Kimmel
@note:      Created on Apr 11, 2013
@license:   MIT License
@summary:   Various functions and utility methods.

"""


# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
# from Modules.Core.data_objects import PyHouseData
from Modules.Core.setup_logging import LOGGING_DICT
from Modules.Utilities import tools
from Modules.Lighting.lighting_lights import LLApi
from Modules.Families.family import API as familyAPI
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


class Print_01(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_EMPTY))
        self.m_api = Logger.API()

    def test_01_String(self):
        l_str = 'String A fairly long String that has no end, at least a fairly long one.'
        PrettyPrintAny(l_str, 'String')
        PrettyPrintAny(l_str, 'String', 15)

    def test_02_Unicode(self):
        l_uc = u'A longish unicode string'
        PrettyPrintAny(l_uc, 'Unicode')
        PrettyPrintAny(l_uc, 'Unicode', 20)

    def test_03_Dict(self):
        l_obj = LOGGING_DICT
        PrettyPrintAny(l_obj, 'A Dict')

    def test_04_XML(self):
        l_xml = self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        PrettyPrintAny(l_xml, 'XML')

    def test_05_Obj(self):
        l_obj = self.m_pyhouse_obj
        PrettyPrintAny(l_obj, 'Obj')

    def test_06_List(self):
        l_lst = [ 'AA', 1, {'a' : 1}, 'BB']
        PrettyPrintAny(l_lst, 'List')

    def test_11_any(self):
        l_any = {'abc': 'Long A B C', 'def' : 'Another long thing.'}
        PrettyPrintAny(l_any)


class Test_02_Find(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = tools.GetPyhouse(self.m_pyhouse_obj)
        self.m_light_api = LLApi(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = familyAPI().build_lighting_family_info()
        self.m_pyhouse_obj.House.DeviceOBJs.Lights = self.m_light_api.read_all_lights_xml(self.m_xml.light_sect)

    def test_01_Setup(self):
        l_loc = self.m_api.Location().Latitude
        print(l_loc)
        PrettyPrintAny(self.m_pyhouse_obj.House.DeviceOBJs, 'Devices')
        PrettyPrintAny(self.m_pyhouse_obj.House.DeviceOBJs.Lights, 'Lights')

    def test_02_FindObj(self):
        l_obj = tools.get_light_object(self.m_pyhouse_obj, 'Insteon Light', None)
        PrettyPrintAny(l_obj, 'Light Obj')
        self.assertIsNotNone(l_obj, 'Must be a light obj')

    def test_03_FindBadObj(self):
        l_obj = tools.get_light_object(self.m_pyhouse_obj, 'NoSuchName', None)
        PrettyPrintAny(l_obj, 'Light Obj')
        self.assertIsNone(l_obj, 'Should be None')

# ## END DBK
