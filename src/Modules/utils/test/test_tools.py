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
from Modules.Core.data_objects import PyHouseData, HouseData
from Modules.utils import tools
from Modules.lights import lighting_lights
from src.test import xml_data
from Modules.utils.tools import PrettyPrintXML, PrettyPrintObject, PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.HouseData = HouseData()
        self.m_pyhouse_obj.XmlRoot = self.m_root_xml

        self.m_houses_xml = self.m_root_xml.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')
        self.m_schedules_xml = self.m_house_xml.find('Schedules')
        self.m_schedule_xml = self.m_schedules_xml.find('Schedule')
        # print('SetupMixin setUp ran')


class Test_01_PrettyPrint(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_PrettyPrintObjects(self):
        l_obj = PyHouseData()
        PrettyPrintObject(l_obj)

    def test_02_PrettyPrintXML(self):
        l_xml = self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        PrettyPrintXML(l_xml)

    def test_03_any(self):
        l_any = {'abc': 'Long A B C', 'def' : 'Another long thing.'}
        PrettyPrintAny(l_any)


class Test_02_PrettyPrint(SetupMixin, unittest.TestCase):

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)

    def test_0201_GetLightObject(self):
        self.m_pyhouse_obj.HouseData.Lights = lighting_lights.LightingAPI(self.m_pyhouse_obj).read_lights_xml(self.m_pyhouse_obj)
        l_obj = tools.get_light_object(self.m_pyhouse_obj.HouseData, name = 'lr_cans', key = None)
        PrettyPrintAny(l_obj)

# ## END DBK
