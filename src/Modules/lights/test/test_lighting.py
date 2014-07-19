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
from test import xml_data, test_mixin


class SetupMixin(object):
    """
    """

    def setUp(self):
        test_mixin.Setup()
        self.m_pyhouse_obj = test_mixin.SetupPyHouseObj().BuildPyHouse()


class Test_02_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)

        self.m_house_div_xml = self.m_root_xml.find('HouseDivision')
        self.m_light_sect_xml = self.m_house_div_xml.find('LightSection')
        self.m_light_xml = self.m_light_sect_xml.find('Light')
        self.m_light_obj = LightData()

        self.m_api = lighting.API()

    def test_0202_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_house_div_xml.tag, 'HouseDivision', 'XML - No Houses section')
        self.assertEqual(self.m_light_sect_xml.tag, 'LightSection', 'XML - No Lights section')
        self.assertEqual(self.m_light_xml.tag, 'Light', 'XML - No Light')

    def test_0211_read_lighting(self):
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse_obj', 120)
        PrettyPrintAny(self.m_pyhouse_obj.Xml, 'PyHouse_obj.Xml', 120)
        self.m_api._read_lighting_xml(self.m_pyhouse_obj)

    def test_0212_write_lighting(self):
        l_obj = self.m_api._read_lighting_xml(self.m_pyhouse_obj)
        self.m_api._write_lighting_xml(l_obj)


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
