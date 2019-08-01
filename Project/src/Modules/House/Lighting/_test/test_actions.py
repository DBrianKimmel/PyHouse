"""
@name:      PyHouse/src/Modules/Lighting/_test/test_lighting_actions.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep 3, 2015
@Summary:

Passed all 5 tests - DBK - 2019-01-20

"""
from Modules.Housing.Lighting.lighting_xml import LightingXML

__updated__ = '2019-01-23'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Housing.Lighting.lighting_controllers import XML as controllerXML
from Modules.Housing.Lighting.lighting_lights import API as lightAPI, XML as lightXML
from Modules.Housing.Lighting.test.xml_lights import XML_LIGHT_SECTION, TESTING_LIGHT_SECTION
from Modules.Housing.Lighting.test.xml_lighting import XML_LIGHTING
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_lighting_actions')


class A1_Api(SetupMixin, unittest.TestCase):
    """
    Test Staticmethods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_DoSchedule(self):
        pass

    def test_02_ChangeLight(self):
        pass


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_xml = XML_LIGHTING
        # print(l_xml)
        self.assertEqual(l_xml[:17], '<LightingSection>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_LIGHT_SECTION)
        # print(PrettyFormatAny.form(l_xml, 'A2-02-A Parsed'))
        self.assertEqual(l_xml.tag, TESTING_LIGHT_SECTION)


class B1_X(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_lights = lightXML().read_all_lights_xml(self.m_pyhouse_obj)

    def test_01_Base(self):
        """ Write out the XML file for the Base controller
        """
        # l_xml = LightingXML()._write_base_device(self.m_controllers[0])
        # print(PrettyFormatAny.form(l_xml, 'C1-01-A - Base'))

# ## END DBK
