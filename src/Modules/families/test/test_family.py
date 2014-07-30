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
from Modules.Core.data_objects import PyHouseData, HouseObjs
from Modules.families import family
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.utils.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_02_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()
        # self.m_api = lighting_controllers.ControllersAPI(self.m_pyhouse_obj)
        # self.m_controller_obj = ControllerData()

    def test_0201_ValidFamilies(self):
        self.assertEqual(family.VALID_FAMILIES[0], 'Insteon')
        self.assertEqual(family.VALID_FAMILIES[1], 'UPB')
        self.assertEqual(family.VALID_FAMILIES[2], 'X10')

    def test_0202_build_one(self):
        l_family_obj = self.m_api.build_one_family('Insteon')
        PrettyPrintAny(l_family_obj)
        self.assertEqual(l_family_obj.Name, 'Insteon', 'Invalid name')
        self.assertEqual(l_family_obj.ModuleName, 'Device_Insteon', 'Invalid Module Name')
        self.assertEqual(l_family_obj.PackageName, 'Modules.families.Insteon', 'Invalid Package Name')

    def test_0203_import_one(self):
        l_family_obj = self.m_api.import_one_module('Insteon')
        self.assertNotEqual(l_family_obj.API, None, 'Error importing module Insteon')
        pass

    def test_0204_import(self):
        l_family_obj = self.m_api.build_one_family('Insteon')
        l_ret = self.m_api.import_module(l_family_obj)
        self.assertNotEqual(l_ret, None, 'Error importing module Insteon')
        pass

    def test_0211_build_family(self):
        self.m_api.build_lighting_family_info()
        pass

    def test_0212_start_family(self):
        l_family_obj = self.m_api.build_lighting_family_info()
        l_family_obj = self.m_api.build_one_family('Insteon')
        l_ret = self.m_api.import_module(l_family_obj)
        self.assertNotEqual(l_ret, None, 'Error importing module Insteon')
        pass

    def test_0213_stop_family(self):
        l_family_obj = self.m_api.build_one_family('Insteon')
        l_ret = self.m_api.import_module(l_family_obj)
        self.assertNotEqual(l_ret, None, 'Error importing module Insteon')
        pass

    def test_0221_BuildXmlName(self):

        pass

# ## END DBK
