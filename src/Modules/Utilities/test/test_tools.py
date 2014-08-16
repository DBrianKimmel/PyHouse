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
from Modules.utils import tools
from Modules.lights import lighting_lights
from Modules.families import family
from src.test import xml_data, test_mixin
from Modules.utils.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self):
        test_mixin.Setup()
        self.m_pyhouse_obj = test_mixin.SetupPyHouseObj().BuildPyHouse()
        # self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()


class Test_01_PrettyPrint(SetupMixin, unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_PrettyPrintObjects(self):
        l_obj = PyHouseData()
        PrettyPrintAny(l_obj, 'Some Obj')

    def test_02_PrettyPrintXML(self):
        l_xml = self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        PrettyPrintAny(l_xml, 'XML')

    def test_03_any(self):
        l_any = {'abc': 'Long A B C', 'def' : 'Another long thing.'}
        PrettyPrintAny(l_any)


class Test_02_PrettyPrint(SetupMixin, unittest.TestCase):

    def _load_family(self):
        l_family = family.API().build_lighting_family_info()
        self.m_pyhouse_obj.House.OBJs.FamilyData = l_family
        return l_family

    def _load_lights(self, p_light_sect_xml):
        l_family = self._load_family()
        l_light_api = lighting_lights.LightingLightsAPI(self.m_pyhouse_obj)
        l_lights = l_light_api.read_all_lights_xml(p_light_sect_xml)
        PrettyPrintAny(l_lights, 'Lights', 80)
        self.m_pyhouse_obj.House.OBJs.Lights = l_lights
        self.m_pyhouse_obj.House.OBJs.FamilyData = l_family

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)
        self.m_house_div_xml = self.m_root_xml.find('HouseDivision')
        self.m_computer_div_xml = self.m_root_xml.find('ComputerDivision')
        self.m_light_sect_xml = self.m_house_div_xml.find('LightSection')
        self.m_light_xml = self.m_light_sect_xml.find('Light')

    def test_0201_GetLightObject(self):
        self._load_lights(self.m_light_sect_xml)
        PrettyPrintAny(self.m_pyhouse_obj, "PyHouse", 120)
        PrettyPrintAny(self.m_pyhouse_obj.House, "PyHouse.House", 100)
        PrettyPrintAny(self.m_pyhouse_obj.House.OBJs, "PyHouse.House.OBJs", 100)
        PrettyPrintAny(self.m_pyhouse_obj.House.OBJs.Lights, "PyHouse.House.OBJs.Lights", 80)
        l_obj = tools.get_light_object(self.m_pyhouse_obj, name = 'lr_cans', key = None)
        PrettyPrintAny(l_obj, 'Light Obj', 80)
        self.assertEqual(l_obj.Name, 'lr_cans')

# ## END DBK
