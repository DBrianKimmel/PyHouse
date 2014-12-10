"""
@name: PyHouse/src/Modules/lights/test/test_lighting_core.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on May 4, 2014
@summary: This module is for testing lighting Core.

Despite its name as "Lighting" this module is also capable of reading and writing
other devices such as thermostats, irrigation systems and pool systems to name a few.

Notice that devices have a lot of configuration entries is XML.  This module only deals with
the "Core" definitions.

Tests all working OK - DBK 2014-07-27
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import LightData, ButtonData, ControllerData
from Modules.Lighting.lighting_core import ReadWriteConfigXml
from Modules.Families import family
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny

XML = xml_data.XML_LONG



class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)



class C01_FindXML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self, self.m_root_xml)
        SetupPyHouseObj().BuildXml(self.m_root_xml)
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_button_obj = ButtonData()
        self.m_controller_obj = ControllerData()
        self.m_light_obj = LightData()
        self.m_api = ReadWriteConfigXml()

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse_obj', 120)
        PrettyPrintAny(self.m_xml, 'XML', 120)
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No Houses section')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection', 'XML - No Lights section')
        self.assertEqual(self.m_xml.light.tag, 'Light', 'XML - No Light')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection', 'XML - No Controller section')
        self.assertEqual(self.m_xml.controller.tag, 'Controller', 'XML - No Controller')
        self.assertEqual(self.m_xml.button_sect.tag, 'ButtonSection', 'XML - No Buttons section')
        self.assertEqual(self.m_xml.button.tag, 'Button', 'XML - No Button')



class C02_ReadXML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self, self.m_root_xml)
        SetupPyHouseObj().BuildXml(self.m_root_xml)
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_button_obj = ButtonData()
        self.m_controller_obj = ControllerData()
        self.m_light_obj = LightData()
        self.m_api = ReadWriteConfigXml()

    def test_01_BaseLight(self):
        """ Read in the xml file and fill in the lights
        """
        l_base = self.m_api.read_base_lighting_xml(self.m_light_obj, self.m_xml.light)
        PrettyPrintAny(l_base, 'ReadBaseLighting', 120)
        self.assertEqual(l_base.Name, 'outside_front', 'Bad Name')
        self.assertEqual(l_base.Key, 0, 'Bad Key')
        self.assertEqual(l_base.Active, True, 'Bad Active')
        self.assertEqual(l_base.Comment, 'SwitchLink On/Off', 'Bad Comments')
        self.assertEqual(l_base.Coords, "['0', '0']", 'Bad Coords')
        self.assertEqual(l_base.IsDimmable, False, 'Bad Dimmable')
        self.assertEqual(l_base.ControllerFamily, 'Insteon', 'Bad ControllerFamily')
        self.assertEqual(l_base.RoomName, 'Foyer', 'Bad Room Name')

    def test_02_ReadBaseController(self):
        """ Read in the xml file and fill in the lights
        """
        l_base = self.m_api.read_base_lighting_xml(self.m_light_obj, self.m_xml.controller)
        PrettyPrintAny(l_base, 'ReadBaseLighting', 120)
        self.assertEqual(l_base.Name, 'PLM_1', 'Bad Name')
        self.assertEqual(l_base.Key, 0, 'Bad Key')
        self.assertEqual(l_base.Active, False, 'Bad Active')
        self.assertEqual(l_base.Comment, 'Dongle using serial converter 067B:2303', 'Bad Comments')
        self.assertEqual(l_base.Coords, "None", 'Bad Coords')
        self.assertEqual(l_base.IsDimmable, False, 'Bad Dimmable')
        self.assertEqual(l_base.ControllerFamily, 'Insteon', 'Bad ControllerFamily')
        self.assertEqual(l_base.RoomName, 'Office', 'Bad Room Name')

    def test_03_ReadBaseButton(self):
        """ Read in the xml file and fill in the lights
        """
        l_base = self.m_api.read_base_lighting_xml(self.m_button_obj, self.m_xml.button)
        PrettyPrintAny(l_base, 'ReadBaseLighting', 120)
        self.assertEqual(l_base.Name, 'kpl_1_A', 'Bad Name')
        self.assertEqual(l_base.Key, 0, 'Bad Key')
        self.assertEqual(l_base.Active, False, 'Bad Active')
        self.assertEqual(l_base.Comment, 'KeypadLink Button A', 'Bad Comments')
        self.assertEqual(l_base.Coords, "None", 'Bad Coords')
        self.assertEqual(l_base.IsDimmable, False, 'Bad Dimmable')
        self.assertEqual(l_base.ControllerFamily, 'Insteon', 'Bad ControllerFamily')
        self.assertEqual(l_base.RoomName, 'Master Bath', 'Bad Room Name')



class C03_WriteXML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self, self.m_root_xml)
        SetupPyHouseObj().BuildXml(self.m_root_xml)
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_button_obj = ButtonData()
        self.m_controller_obj = ControllerData()
        self.m_light_obj = LightData()
        self.m_api = ReadWriteConfigXml()

    def test_01_BaseLight(self):
        """ Read in the xml file and fill in the lights
        """
        # l_xml = ET.Element('Lights')
        l_base = self.m_api.read_base_lighting_xml(self.m_light_obj, self.m_xml.light)
        l_xml = self.m_api.write_base_lighting_xml(l_base)
        PrettyPrintAny(l_xml, 'Lighting Core')

    def test_02_BaseController(self):
        """ Read in the xml file and fill in the lights
        """
        # l_xml = ET.Element('Lights')
        l_base = self.m_api.read_base_lighting_xml(self.m_light_obj, self.m_xml.controller)
        l_xml = self.m_api.write_base_lighting_xml(l_base)
        PrettyPrintAny(l_xml, 'Lighting Core')

    def test_03_BaseButton(self):
        """ Read in the xml file and fill in the lights
        """
        # l_xml = ET.Element('Lights')
        l_base = self.m_api.read_base_lighting_xml(self.m_light_obj, self.m_xml.button)
        l_xml = self.m_api.write_base_lighting_xml(l_base)
        PrettyPrintAny(l_xml, 'Lighting Core')



class C04_EmptyXML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML before anything has been defined.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_EMPTY)
        SetupMixin.setUp(self, self.m_root_xml)
        SetupPyHouseObj().BuildXml(self.m_root_xml)
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_light_obj = LightData()
        self.m_api = ReadWriteConfigXml()

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse_obj', 120)
        PrettyPrintAny(self.m_xml, 'XML', 120)
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')



class C05_EmptyXML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_EMPTY)
        SetupMixin.setUp(self, self.m_root_xml)
        SetupPyHouseObj().BuildXml(self.m_root_xml)
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_light_obj = LightData()
        self.m_api = ReadWriteConfigXml()

    def test_02_ReadBaseXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_base = self.m_api.read_base_lighting_xml(self.m_light_obj, self.m_xml.light)
        PrettyPrintAny(l_base, 'ReadBaseLighting', 120)
        self.assertEqual(l_base.Name, 'Missing Name', 'Bad Name')
        self.assertEqual(l_base.Key, 0, 'Bad Key')
        self.assertEqual(l_base.Active, False, 'Bad Active')
        # self.assertEqual(l_base.Comment, 'None', 'Bad Comments')
        self.assertEqual(l_base.Coords, 'None', 'Bad Coords')
        self.assertEqual(l_base.IsDimmable, False, 'Bad Dimmable')
        self.assertEqual(l_base.ControllerFamily, 'None', 'Bad ControllerFamily')
        self.assertEqual(l_base.RoomName, 'None', 'Bad Room Name')



class C06_EmptyXML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_EMPTY)
        SetupMixin.setUp(self, self.m_root_xml)
        SetupPyHouseObj().BuildXml(self.m_root_xml)
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_light_obj = LightData()
        self.m_api = ReadWriteConfigXml()

    def test_01_WriteBaseXml(self):
        """ Read in the xml file and fill in the lights
        """
        # l_xml = ET.Element('Lights')
        l_xml = self.m_api.write_base_lighting_xml(self.m_light_obj)
        PrettyPrintAny(l_xml, 'Lighting Core')

# ## END DBK
