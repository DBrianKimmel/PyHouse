"""
@name: PyHouse/src/Modules/lights/test/test_lighting.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@note: Created on Apr 9, 2013
@license: MIT License
@summary: Handle the home lighting system automation.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import LightData
from Modules.lights import lighting
from Modules.families import family
from Modules.utils.tools import PrettyPrintAny
from test import xml_data
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_02_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self, self.m_root_xml)
        SetupPyHouseObj().BuildXml(self.m_root_xml)
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_light_obj = LightData()
        self.m_api = lighting.API()

    def test_0202_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No Houses section')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection', 'XML - No Lights section')
        self.assertEqual(self.m_xml.light.tag, 'Light', 'XML - No Light')

    def test_0211_read_lighting(self):
        self.m_api._read_lighting_xml(self.m_pyhouse_obj)
        PrettyPrintAny(self.m_pyhouse_obj.House.OBJs, 'PyHouse_obj.House.OBJs', 120)
        PrettyPrintAny(self.m_pyhouse_obj.House.OBJs.Lights, 'PyHouse_obj-Lights', 120)
        self.assertEqual(self.m_pyhouse_obj.House.OBJs.Lights[0].Name, 'outside_front')

    def test_0212_write_lighting(self):
        l_obj = self.m_api._read_lighting_xml(self.m_pyhouse_obj)
        self.m_api._write_lighting_xml(self.m_pyhouse_obj.House.OBJs, self.m_xml.house_div)


# class Test_03_ReadXMLEmpty(SetupMixin, unittest.TestCase):
#    """ This section tests the reading and writing of XML used by node_local.
#    """

    # def XsetUp(self):
    #    self.m_root_xml = ET.fromstring(xml_data.XML_EMPTY)
    #    SetupMixin.setUp(self)

    # def Xtest_0301_read_lighting(self):
    #    pass

    # def Xtest_0302_write_lighting(self):
    #    pass

# ## END DBK
