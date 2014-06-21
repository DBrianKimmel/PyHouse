"""
@name: PyHouse/src/Modules/families/test/test_family.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@note: Created on May 17, 2013
@license: MIT License
@summary: This module is for testing family.
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, HouseData
from Modules.families import family
from src.test import xml_data
from Modules.utils.tools import PrettyPrintAny

XML = xml_data.XML_LONG


class Test_01_Families(unittest.TestCase):

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.House.OBJs = HouseData()
        self.m_pyhouse_obj.XmlRoot = self.m_root = ET.fromstring(XML)
        self.m_houses = self.m_root.find('Houses')
        self.m_house = self.m_houses.find('House')
        # self.m_house_obj = RoomData()
        self.m_api = family.API()

    def test_0101_ValidFamilies(self):
        self.assertEqual(family.VALID_FAMILIES[0], 'Insteon')
        self.assertEqual(family.VALID_FAMILIES[1], 'UPB')
        self.assertEqual(family.VALID_FAMILIES[2], 'X10')

    def test_0102_build_one(self):
        l_family_obj = self.m_api.build_one_family('Insteon')
        PrettyPrintAny(l_family_obj)
        self.assertEqual(l_family_obj.Name, 'Insteon', 'Invalid name')
        self.assertEqual(l_family_obj.ModuleName, 'Device_Insteon', 'Invalid Module Name')
        self.assertEqual(l_family_obj.PackageName, 'Modules.families.Insteon', 'Invalid Package Name')

    def test_0103_import_one(self):
        l_family_obj = self.m_api.import_one_module('Insteon')
        self.assertNotEqual(l_family_obj.API, None, 'Error importing module Insteon')
        pass

    def test_0104_import(self):
        l_family_obj = self.m_api.build_one_family('Insteon')
        l_ret = self.m_api.import_module(l_family_obj)
        self.assertNotEqual(l_ret, None, 'Error importing module Insteon')
        pass

    def test_0111_build_family(self):
        self.m_api.build_lighting_family_info()
        pass

    def test_0112_start_family(self):
        l_family_obj = self.m_api.build_lighting_family_info()
        l_family_obj = self.m_api.build_one_family('Insteon')
        l_ret = self.m_api.import_module(l_family_obj)
        self.assertNotEqual(l_ret, None, 'Error importing module Insteon')
        pass

    def test_0113_stop_family(self):
        l_family_obj = self.m_api.build_one_family('Insteon')
        l_ret = self.m_api.import_module(l_family_obj)
        self.assertNotEqual(l_ret, None, 'Error importing module Insteon')
        pass

# ## END DBK
